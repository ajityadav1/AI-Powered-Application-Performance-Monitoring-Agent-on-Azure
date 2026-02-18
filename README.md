# Observability Agent with Azure Application Insights

This project provides an observability agent that integrates with Azure Application Insights to monitor and collect telemetry data from your Python applications.

## Features
- Easy integration with Azure Application Insights
- Automatic collection of logs, traces, and metrics
- Custom event and metric tracking
- Configurable via environment variables or code

## Getting Started

### Prerequisites
- Python 3.7 or higher
- An Azure Application Insights resource (Instrumentation Key or Connection String)

### Installation
1. Clone this repository or download the files.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```


### Configuration
You can configure the agent using a `.env` file or by setting environment variables directly.

#### Using a `.env` file
Create a file named `.env` in the project root with the following content:

```
APPINSIGHTS_INSTRUMENTATIONKEY=<your-instrumentation-key>
# or
APPLICATIONINSIGHTS_CONNECTION_STRING=<your-connection-string>
```

#### Using environment variables (PowerShell example)
```powershell
$env:APPINSIGHTS_INSTRUMENTATIONKEY = "<your-instrumentation-key>"
# or
$env:APPLICATIONINSIGHTS_CONNECTION_STRING = "<your-connection-string>"
```


### Usage
1. Ensure your `.env` file is set up or environment variables are configured as above.
2. Import and initialize the observability agent in your Python application:

```python
from observability_appinsights_azure import setup_app_insights

setup_app_insights()
# ...your application code...
```

#### Custom Events and Metrics
You can also track custom events and metrics:

```python
from observability_appinsights_azure import track_event, track_metric

track_event("MyCustomEvent", {"property1": "value1"})
track_metric("MyCustomMetric", 42)
```

#### Running the Agent
If you have a main script, just run it as usual:

```powershell
python your_script.py
```


## File Structure
- `observability_appinsights_azure.py`: Main module for integrating with Azure Application Insights.
- `requirements.txt`: Python dependencies.
- `.env`: (Optional) Environment variable configuration file.
- `kql/`: Sample Kusto Query Language files for querying Application Insights data.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements.

## License
This project is licensed under the MIT License.
