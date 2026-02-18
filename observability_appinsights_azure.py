
import os
import requests
import json
from openai import AzureOpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-05-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def query_app_insights():
    # Allow user to specify which KQL file to use
    kql_folder = os.path.join(os.path.dirname(__file__), "kql")
    kql_file = os.environ.get("KQL_FILE", "performanceCounters.kql")  # Default file
    kql_path = os.path.join(kql_folder, kql_file)
    with open(kql_path, "r", encoding="utf-8") as f:
        kql_query = f.read()
    url = f"https://api.applicationinsights.io/v1/apps/{APP_ID}/query"
    headers = {"x-api-key": API_KEY}
    response = requests.post(url, headers=headers, json={"query": kql_query})
    response.raise_for_status()
    return response.json()

def analyze_with_gpt(timeseries):
    prompt = f"""
    You are an observability assistant analyzing application telemetry from Azure App Insights.

    Telemetry data (JSON timeseries):
    {json.dumps(timeseries, indent=2)}

    Instructions:
    1. Convert the above telemetry into a markdown table with the following columns:
       | CPU (%) | Requests | Failures | Failure Rate (%) | Avg Response Time (ms) | OOM Errors | Socket Exceptions |
       - Convert Memory from bytes to MB (divide by 1024*1024).
       - Round CPU and Memory values to 2 decimal places.
    2. Identify if failure rate, response time, or CPU usage show a rising trend.
    3. Predict if the application may crash or degrade soon based on OOM errors, CPU, and Memory pressure.
    4. Answer in 2–3 concise sentences summarizing the trend.
    5. Always end with this exact line (no extra words):
       Likely issue soon: Yes/No
    """

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are an expert SRE/DevOps assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0
    )
    return response.choices[0].message.content

def send_teams_alert(message: str):
    if not TEAMS_WEBHOOK_URL:
        print("⚠️ Teams webhook not set, skipping alert.")
        return
    # Wrap message in triple backticks to preserve markdown table formatting in Teams
    formatted_message = f"🚨 Predictive Alert:\n```markdown\n{message}\n```"
    payload = {"text": formatted_message}
    requests.post(TEAMS_WEBHOOK_URL,
                  headers={"Content-Type": "application/json"},
                  data=json.dumps(payload))

if __name__ == "__main__":
    print("🔎 Querying Application Insights...")
    results = query_app_insights()
    timeseries = results.get("tables", [])[0].get("rows", [])
    print("📊 Raw telemetry rows:", timeseries)

    if not timeseries:
        print("No telemetry data returned!")
    else:
        analysis = analyze_with_gpt(timeseries)
        print("🤖 Analysis:\n", analysis)
        send_teams_alert(analysis)
        # if "Likely issue soon: Yes" in analysis:
        #     send_teams_alert(analysis)
        #     print("✅ Alert sent to Teams.")
        # else:
        #     print("✅ No alert needed.")
