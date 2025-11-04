# Kairo Python SDK

A Python SDK for Kairo, providing telemetry and monitoring capabilities.

## Installation

```bash
pip install microsoft-kairo
```

## Usage

### Basic Configuration

```python
import microsoft_kairo

# Configure Kairo with console output (default)
microsoft_kairo.configure_kairo(
    service_name="my-service",
    service_namespace="my-namespace",
    agent_id="agent-123"
)
```

### Advanced Configuration

```python
import microsoft_kairo

# Configure with Azure Monitor
microsoft_kairo.configure_kairo(
    service_name="my-service",
    service_namespace="my-namespace",
    agent_id="agent-123",
    exporter_type="azure_monitor",
    exporter_endpoint="InstrumentationKey=your-instrumentation-key"
)

# Configure with OTLP exporter
microsoft_kairo.configure_kairo(
    service_name="my-service",
    service_namespace="my-namespace", 
    agent_id="agent-123",
    exporter_type="otlp",
    exporter_endpoint="http://localhost:4317"
)
```

### Available Exports

- `configure_kairo()`: Main configuration function
- `KairoSpanProcessor`: Custom span processor class
- `KAIRO_AGENT_ID_KEY`: Constant for agent ID attribute key

## Optional Dependencies

- `otlp`: OpenTelemetry OTLP exporter
- `jaeger`: Jaeger exporter
- `azure`: Azure Monitor exporter
- `all`: All optional dependencies

Install with optional dependencies:

```bash
pip install microsoft-kairo[azure]
```

## Building and publishing the package

Build the package with:

```
uv build --wheel
```

which will generate a date-based wheel package in the `dist/` folder. Ex.: `dist\microsoft_kairo-2025.10.7+preview.15276-py3-none-any.whl`.

Then publish it with:

```
uv run twine upload --config-file .\.pypirc -r Agent365 dist/*
```

## 📋 **Telemetry**

Data Collection. The software may collect information about you and your use of the software and send it to Microsoft. Microsoft may use this information to provide services and improve our products and services. You may turn off the telemetry as described in the repository. There are also some features in the software that may enable you and Microsoft to collect data from users of your applications. If you use these features, you must comply with applicable law, including providing appropriate notices to users of your applications together with a copy of Microsoft’s privacy statement. Our privacy statement is located at https://go.microsoft.com/fwlink/?LinkID=824704. You can learn more about data collection and use in the help documentation and our privacy statement. Your use of the software operates as your consent to these practices.