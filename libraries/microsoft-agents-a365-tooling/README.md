# microsoft-agents-a365-tooling

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-tooling?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-tooling?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling)

Core tooling functionality for MCP (Model Context Protocol) tool server management in Microsoft Agents 365 applications. This package provides the foundation for discovering, registering, and managing tool servers across different AI frameworks.

## Installation

```bash
pip install microsoft-agents-a365-tooling
```

## Usage

### Tool Server Discovery

```python
from microsoft_agents_a365.tooling.services import McpToolServerConfigurationService

tool_service = McpToolServerConfigurationService()

# List all available tool servers for an agent
tool_servers = await tool_service.list_tool_servers(agent_instance_id, environment_id, auth_token)

for server in tool_servers:
    print(f"Tool Server: {server.mcp_server_name}")
    print(f"  Server URL: {server.url}")
```

### Get MCP Client Tools

```python
# Get tools from a specific server
mcp_tools = await tool_service.get_mcp_client_tools(
    turn_context,
    server,
    environment_id,
    auth_token)
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
