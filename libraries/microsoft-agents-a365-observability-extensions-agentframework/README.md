# microsoft-agents-a365-observability-extensions-agentframework

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-observability-extensions-agentframework?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-agentframework)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-observability-extensions-agentframework?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-agentframework)

Observability extensions for Microsoft Agent Framework. This package provides OpenTelemetry tracing integration specifically for Agent Framework-based applications.

## Installation

```bash
pip install microsoft-agents-a365-observability-extensions-agentframework
```

## Usage

### Basic Configuration

```python
from microsoft_agents_a365.observability.extensions.agentframework import (
    AgentFrameworkTraceInstrumentor
)

# Initialize instrumentor
instrumentor = AgentFrameworkTraceInstrumentor()

# Instrument your agent framework application
instrumentor.instrument()

# Your agent code runs with automatic tracing
# ...

# Optional: Uninstrument when done
instrumentor.uninstrument()
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
