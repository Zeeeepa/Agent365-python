# microsoft-agents-a365-observability-core

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-observability-core?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-core)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-observability-core?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-core)

Telemetry, tracing, and monitoring components for AI agents built on OpenTelemetry. This package provides structured spans for agent invocation, tool execution, and LLM inference with context propagation and pluggable exporters.

## Installation

```bash
pip install microsoft-agents-a365-observability-core
```

## Usage

### Basic Configuration

```python
from microsoft_agents_a365.observability.core import configure, get_tracer

# Configure observability with service details
configure(
    service_name="my-agent-service",
    service_namespace="my.namespace"
)

# Get tracer instance
tracer = get_tracer()
```

### Using Tracing Scopes

```python
from microsoft_agents_a365.observability.core import (
    InvokeAgentScope,
    ExecuteToolScope,
    InferenceScope,
    InvokeAgentDetails,
    ToolCallDetails,
    InferenceCallDetails,
    AgentDetails,
    TenantDetails,
    Request
)

# Trace agent invocation
agent_details = AgentDetails(agent_id="my-agent", agent_name="My Agent")
tenant_details = TenantDetails(tenant_id="tenant-123")
request = Request(content="User query")

invoke_details = InvokeAgentDetails(
    details=agent_details,
    session_id="session-42"
)

with InvokeAgentScope.start(invoke_details, tenant_details, request):
    # Agent execution code here
    result = await process_request()

# Trace tool execution
tool_details = ToolCallDetails(
    tool_name="search_tool",
    tool_type="function"
)

with ExecuteToolScope.start(tool_details, agent_details, tenant_details):
    # Tool execution code
    search_result = await execute_search()

# Trace LLM inference
inference_details = InferenceCallDetails(
    operationName="chat",
    model="gpt-4"
)

with InferenceScope.start(inference_details, agent_details, tenant_details, request):
    # LLM call
    response = await llm.complete(prompt)
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.

