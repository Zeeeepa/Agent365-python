# Microsoft Agent 365 Tooling Extensions - Agent Framework
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-agentframework.svg)](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-agentframework)

Agent Framework integration tools and MCP tool registration services for AI agent applications built with the Microsoft Agent 365 SDK. Provides specialized tooling for integrating MCP (Model Context Protocol) servers with Agent Framework agents and projects.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The Agent Framework tooling extensions specifically provide integration with Microsoft Agent Framework, enabling seamless registration and management of MCP tool servers within the Agent Framework ecosystem.

## Key Features

✅ **Agent Framework Integration** - Native integration with Microsoft Agent Framework  
✅ **MCP Tool Registration** - Automatic registration of MCP servers with Agent Framework agents  
✅ **Azure Identity Support** - Built-in Azure authentication with DefaultAzureCredential  
✅ **Tool Resource Management** - Comprehensive management of tool definitions and resources  
✅ **Multi-Environment Support** - Support for development and production deployment scenarios  
✅ **Enterprise Ready** - Production-grade tooling for Agent Framework-based agent deployments  

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-agentframework
```

### Prerequisites

The Agent Framework tooling extensions require the Agent Framework Core package:

```bash
# Core Agent Framework (includes Azure OpenAI and OpenAI support by default)
# also includes workflows and orchestrations
pip install agent-framework-core --pre
```

**Optional Agent Framework packages:**
```bash
# Core + Azure AI integration
pip install agent-framework-azure-ai --pre

# Core + Microsoft Copilot Studio integration
pip install agent-framework-copilotstudio --pre

# Core + both Microsoft Copilot Studio and Azure AI integration
pip install agent-framework-microsoft agent-framework-azure-ai --pre
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 Agent Framework Tooling Extensions enable seamless integration between MCP tool servers and Agent Framework agents. Key concepts include:

- **MCP Tool Registration**: Automatic registration of tool definitions with Agent Framework
- **Agent Resource Management**: Management of agent resources and configurations
- **Tool Discovery**: Dynamic discovery and registration of available tools
- **Service Integration**: Integration with various service providers and backends

### Basic Usage

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from microsoft_agents_a365.tooling.extensions.agentframework import (
    McpToolRegistrationService,
)

async def main():
    # Initialize the MCP tool registration service
    service = McpToolRegistrationService()
    
    # Create Azure OpenAI chat client
    chat_client = AzureOpenAIChatClient(
        api_key='',
        endpoint='',
        deployment_name='',
        api_version='',
    )
    
    # Create agent with MCP tools from all configured servers
    agent = await service.add_tool_servers_to_agent(
        chat_client=chat_client,
        agent_instructions="You are a helpful assistant that can provide weather and restaurant information.",
        initial_tools=[],  # Your existing tools
        agent_user_id="user-123",
        environment_id="prod",
        auth_token="your-auth-token"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Configuration

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from microsoft_agents_a365.tooling.extensions.agentframework import (
    McpToolRegistrationService,
)

async def main():
    # Initialize with custom logger and credentials
    import logging
    from azure.identity import DefaultAzureCredential
    
    logger = logging.getLogger("my-agent")
    credential = DefaultAzureCredential()
    
    service = McpToolRegistrationService(
        logger=logger,
        credential=credential
    )
    
    # Create Azure OpenAI chat client
    chat_client = AzureOpenAIChatClient(
        api_key='',
        endpoint='',
        deployment_name='',
        api_version='',
    )
    
    # Define existing tools (if any)
    existing_tools = [
        # Your existing tools go here
    ]
    
    # Create agent with comprehensive instructions and all MCP tools
    agent = await service.add_tool_servers_to_agent(
        chat_client=chat_client,
        agent_instructions="""
        You are a helpful AI assistant with access to various tools and services.
        
        Guidelines:
        1) Always be helpful and accurate
        2) Use available tools when appropriate to provide better assistance
        3) Explain your reasoning when using tools
        
        You have access to MCP (Model Context Protocol) tools that are automatically
        loaded from configured servers. Use these tools to enhance your capabilities.
        """,
        initial_tools=existing_tools,
        agent_user_id="user-123",
        environment_id="production",
        auth_token="your-auth-token"
    )
    
    # The agent now has all MCP tools from configured servers
    print(f"Agent created with {len(agent.tools)} total tools")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The library supports various configuration options through environment variables:

- `AGENT_FRAMEWORK_ENDPOINT`: The Agent Framework endpoint URL
- `AGENT_FRAMEWORK_API_KEY`: API key for Agent Framework authentication
- `MCP_TOOLS_DIRECTORY`: Directory containing MCP tool definitions
- `AGENT_ENVIRONMENT`: Deployment environment (development, staging, production)

## Agent Framework Integration

This library provides deep integration with Microsoft Agent Framework using the `ChatAgent` pattern:

### MCP Tool Server Registration

Automatically register MCP tools from all configured servers with your Agent Framework agents:

```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from microsoft_agents_a365.tooling.extensions.agentframework import (
    McpToolRegistrationService,
)

service = McpToolRegistrationService()

# Create Azure OpenAI chat client
chat_client = AzureOpenAIChatClient(
    api_key='',
    endpoint='',
    deployment_name='',
    api_version='',
)

# Register all MCP tools from configured servers
agent = await service.add_tool_servers_to_agent(
    chat_client=chat_client,
    agent_instructions="You are a helpful assistant with access to various tools.",
    initial_tools=[],  # Your existing tools
    agent_user_id="user-123",
    environment_id="prod",
    auth_token="your-token"
)
```

### How It Works

The `add_tool_servers_to_agent` method:

1. **Discovers MCP Servers**: Uses the MCP server configuration service to find all configured servers
2. **Retrieves Tools**: Connects to each server and retrieves available tool definitions  
3. **Combines Tools**: Merges your existing tools with the MCP tools
4. **Creates New Agent**: Returns a new `ChatAgent` instance with all tools configured

### Agent Configuration

Configure agents with different chat clients:

```python
# Using Azure OpenAI (recommended)
from agent_framework.azure import AzureOpenAIChatClient

chat_client = AzureOpenAIChatClient(
    api_key='',
    endpoint='',
    deployment_name='',
    api_version='',
)

# Alternative: Using OpenAI directly
from agent_framework.openai import OpenAIChatClient
chat_client = OpenAIChatClient()
```

## Development

### Prerequisites

- Python 3.11 or higher
- Agent Framework Core SDK (`agent-framework-core`)
- Azure Identity (for authentication)

### Development Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

### Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run the formatter and linter:
```bash
black microsoft_agents_a365/
ruff check microsoft_agents_a365/
mypy microsoft_agents_a365/
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License. See the [LICENSE](../../LICENSE.md) file for details.

## Support

For support and questions:
- File issues on [GitHub Issues](https://github.com/microsoft/Agent365/issues)
- Check the [documentation](https://github.com/microsoft/Agent365/tree/main/python)
- Join the community discussions

## Related Libraries

This library is part of the Microsoft Agent 365 SDK ecosystem:

- `microsoft-agents-a365-runtime` - Core runtime and utilities
- `microsoft-agents-a365-tooling` - Base tooling framework
- `microsoft-agents-a365-tooling-extensions-openai` - OpenAI integration
- `microsoft-agents-a365-tooling-extensions-semantickernel` - Semantic Kernel integration
- `microsoft-agents-a365-observability-core` - Observability and monitoring