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
