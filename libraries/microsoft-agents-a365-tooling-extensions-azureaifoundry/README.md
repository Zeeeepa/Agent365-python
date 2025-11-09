# microsoft-agents-a365-tooling-extensions-azureaifoundry

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-tooling-extensions-azureaifoundry?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-azureaifoundry)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-tooling-extensions-azureaifoundry?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-azureaifoundry)

Azure AI Foundry specific tools and services for AI agent development. Provides MCP (Model Context Protocol) tool registration service for dynamically adding MCP servers to Azure AI Foundry agents.

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-azureaifoundry
```

## Usage

### Basic MCP Tool Registration

```python
from microsoft_agents_a365.tooling.extensions.azureaifoundry import (
    McpToolRegistrationService
)
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize the tool registration service
mcp_service = McpToolRegistrationService()

# Create Azure AI Project client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    subscription_id="your-subscription-id",
    resource_group_name="your-resource-group",
    project_name="your-project-name"
)

# Add MCP tool servers to agent
agent = await mcp_service.add_tool_servers_to_agent(
    project_client=project_client,
    agent_instructions="You are a helpful assistant",
    agentic_app_id="your-agent-id",
    environment_id="your-environment-id",
    auth=authorization,
    turn_context=turn_context
)

# Use the agent with registered MCP tools
response = await agent.run("Help me with my task")
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
