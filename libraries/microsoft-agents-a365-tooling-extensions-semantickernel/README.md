# microsoft-agents-a365-tooling-extensions-semantickernel

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-tooling-extensions-semantickernel?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-semantickernel)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-tooling-extensions-semantickernel?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-semantickernel)

Semantic Kernel specific tools and services for AI agent development. Provides MCP (Model Context Protocol) tool registration service for dynamically adding MCP servers to Semantic Kernel-based agents.

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-semantickernel
```

## Usage

### Basic MCP Tool Registration

```python
from microsoft_agents_a365.tooling.extensions.semantickernel import (
    McpToolRegistrationService
)
from semantic_kernel import Kernel

# Initialize the tool registration service
mcp_service = McpToolRegistrationService()

# Create Semantic Kernel instance
kernel = Kernel()

# Add MCP tool servers to kernel
await mcp_service.add_tool_servers_to_kernel(
    kernel=kernel,
    agentic_app_id="your-agent-id",
    environment_id="your-environment-id",
    auth=authorization,
    turn_context=turn_context
)

# Use the kernel with registered MCP tools
result = await kernel.invoke("Help me with my task")
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
