# microsoft-agents-a365-observability-extensions-openai

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-observability-extensions-openai?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-openai)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-observability-extensions-openai?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-openai)

Observability extensions for OpenAI Agents SDK. This package provides OpenTelemetry tracing integration for OpenAI Agents-based applications with automatic instrumentation for agent workflows and tool invocations.

## Installation

```bash
pip install microsoft-agents-a365-observability-extensions-openai
```

## Usage

### Basic Configuration

```python
from microsoft_agents_a365.observability.core import configure
from microsoft_agents_a365.observability.extensions.openai import (
    OpenAIAgentsTraceInstrumentor
)

# Configure observability
configure(
    service_name="my-openai-agent",
    service_namespace="ai.agents"
)

# Enable automatic instrumentation
instrumentor = OpenAIAgentsTraceInstrumentor()
instrumentor.instrument()

# Your OpenAI Agents code is now automatically traced
from openai import OpenAI

client = OpenAI()
# All agent operations will be automatically instrumented
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.

configure(
