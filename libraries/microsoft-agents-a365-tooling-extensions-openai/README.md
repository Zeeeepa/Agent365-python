# microsoft-agents-a365-tooling-extensions-openai

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-tooling-extensions-openai?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-openai)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-tooling-extensions-openai?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-tooling-extensions-openai)

OpenAI Agents SDK specific tools and services for AI agent development. Provides MCP (Model Context Protocol) tool registration service for dynamically adding MCP servers to OpenAI Agents SDK-based agents.

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-openai
```

## Usage

### Basic MCP Tool Registration

```python
from microsoft_agents_a365.tooling.extensions.openai import (
    McpToolRegistrationService
)
from agents import Agent

# Initialize the tool registration service
mcp_service = McpToolRegistrationService()

# Create your OpenAI agent
agent = Agent(
    name="my-agent",
    instructions="You are a helpful assistant"
)

# Add MCP tool servers to agent
await mcp_service.add_tool_servers_to_agent(
    agent=agent,
    agentic_app_id="your-agent-id",
    environment_id="your-environment-id",
    auth=authorization,
    context=turn_context
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
