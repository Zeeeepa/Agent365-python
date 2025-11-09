# microsoft-agents-a365-observability-extensions-semantickernel

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-observability-extensions-semantickernel?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-semantickernel)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-observability-extensions-semantickernel?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-semantickernel)

Observability extensions for Semantic Kernel framework. This package provides OpenTelemetry tracing integration for Semantic Kernel-based applications with automatic instrumentation for kernel functions, plugins, and planners.

## Installation

```bash
pip install microsoft-agents-a365-observability-extensions-semantickernel
```

## Usage

### Basic Configuration

```python
from microsoft_agents_a365.observability.core import configure
from microsoft_agents_a365.observability.extensions.semantickernel import (
    SemanticKernelInstrumentor
)

# Configure observability
configure(
    service_name="my-semantic-kernel-agent",
    service_namespace="ai.agents"
)

# Enable automatic instrumentation
instrumentor = SemanticKernelInstrumentor()
instrumentor.instrument()

# Your Semantic Kernel code is now automatically traced
from semantic_kernel import Kernel

kernel = Kernel()
# All kernel operations will be automatically instrumented
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
