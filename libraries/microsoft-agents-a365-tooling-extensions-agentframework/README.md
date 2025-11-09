# microsoft-agents-a365-tooling-extensions-agentframework

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-tooling-extensions-agentframework?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-agentframework)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-tooling-extensions-agentframework?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-agentframework)

Agent Framework specific tools and services for AI agent development. Provides MCP (Model Context Protocol) tool registration service for dynamically adding MCP servers to Agent Framework agents.

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-agentframework
```

## Usage

### Basic MCP Tool Registration

```python
from microsoft_agents_a365.tooling.extensions.agentframework import (
    McpToolRegistrationService
)
from agent_framework.azure import AzureOpenAIChatClient

# Initialize the tool registration service
mcp_service = McpToolRegistrationService()

# Create chat client
chat_client = AzureOpenAIChatClient(
    endpoint="https://your-endpoint.openai.azure.com",
    api_key="your-api-key",
    model="gpt-4"
)

# Add MCP tool servers to agent
agent = await mcp_service.add_tool_servers_to_agent(
    chat_client=chat_client,
    agent_instructions="You are a helpful assistant",
    initial_tools=[],  # Any initial tools
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
