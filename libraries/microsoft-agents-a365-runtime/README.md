# Microsoft Agent 365 Runtime

This package provides telemetry, tracing, and monitoring components for AI agent applications.

## Features

- **Agent Monitoring**: Specialized tracing for AI agent invocations with detailed telemetry
- **Tool Execution Tracking**: Monitor tool executions and function calls with comprehensive metrics  
- **OpenTelemetry Integration**: Built-in OpenTelemetry tracing for standardized observability
- **Azure Monitor Support**: Seamless integration with Azure Monitor for cloud-based monitoring
- **Custom Trace Processors**: Extensible trace processing for custom monitoring requirements

## Quick Start

### Import the observability components
```python
from microsoft_kairo.observability import configure, ExecuteAgentScope
```

### Basic Usage

Configure with Azure Monitor and add agent tracing:
```python
# Configure with Azure Monitor
configure(
    service_name="my-python-agent",
    service_version="1.0.0", 
    exporter="azure_monitor",
    connection_string="your-connection-string"
)

# Add agent tracing
with ExecuteAgentScope.start(agent_id="my-agent") as scope:
    # Your agent logic here
    pass
```

The package provides components for:
- **ExecuteAgentScope**: Track agent execution contexts
- **ExecuteToolScope**: Monitor tool and function calls
- **InferenceScope**: Trace LLM inference operations
- **SpanProcessor**: Custom span processing capabilities
- **DefenderTraceProcessor**: Security-focused trace processing

## Installation

```bash
pip install microsoft-agents-a365-observability
```

## Requirements

- Python 3.9+
- OpenTelemetry API >= 1.20.0
- Compatible with AI agent frameworks