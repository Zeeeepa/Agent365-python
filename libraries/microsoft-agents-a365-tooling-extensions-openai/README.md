# Microsoft Agent 365 Tooling Extensions - OpenAI
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-openai.svg)](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-openai)

OpenAI Agents SDK integration tools and MCP tool registration services for AI agent applications built with the Microsoft Agent 365 SDK. Provides specialized tooling for integrating MCP (Model Context Protocol) servers with OpenAI Agents SDK applications.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The OpenAI tooling extensions specifically provide integration with the OpenAI Agents SDK, enabling seamless registration and management of MCP tool servers within OpenAI-based agent applications.

## Key Features

✅ **OpenAI Agents SDK Integration** - Native integration with OpenAI Agents SDK and framework  
✅ **MCP Tool Registration** - Automatic registration of MCP servers with OpenAI agents  
✅ **Multiple Server Types** - Support for hosted, streamable HTTP, SSE, and stdio MCP servers  
✅ **Dynamic Tool Management** - Runtime addition and management of MCP tool servers  
✅ **Authentication Integration** - Seamless integration with Microsoft Agent 365 authentication  
✅ **Enterprise Ready** - Production-grade tooling for OpenAI-based agent deployments  

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-openai
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 OpenAI Tooling Extensions enable seamless integration between MCP tool servers and OpenAI Agents SDK applications. Key concepts include:

- **MCP Tool Registration**: Automatic registration of MCP servers with OpenAI agents
- **OpenAI Agents Integration**: Native integration with OpenAI Agents SDK framework
- **Multiple Server Types**: Support for various MCP server deployment types
- **Dynamic Tool Management**: Runtime management of tool servers and configurations

### Getting Started

1. Install the package: `pip install microsoft-agents-a365-tooling-extensions-openai`
2. Configure your OpenAI agent application with MCP support
3. Use the MCP tool registration service to add tools to your agents
4. Deploy and manage your OpenAI agents with MCP capabilities

### Basic Usage

```python
from microsoft_agents_a365.tooling.extensions.openai import McpToolRegistrationService
from agents import Agent
from microsoft_agents.hosting.core import Authorization, TurnContext

# Create MCP tool registration service
registration_service = McpToolRegistrationService()

# Add MCP tool servers to your OpenAI agent
await registration_service.add_tool_servers_to_agent(
    agent=your_openai_agent,
    agent_user_id="user-123",
    environment_id="prod",
    auth=authorization_context,
    context=turn_context,
    auth_token="your-auth-token"
)
```

## Core OpenAI Integration Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **McpToolRegistrationService** | Tool Registration | Register MCP servers with OpenAI Agents SDK applications |
| **MCPServerInfo** | Server Configuration | Configuration model for MCP server information and settings |
| **Multiple Server Types** | Server Support | Support for hosted, streamable HTTP, SSE, and stdio servers |
| **Authentication Integration** | Security | Integration with Microsoft Agent 365 authentication systems |

## Supported MCP Server Types

| Server Type | Component | Description |
|-------------|-----------|-------------|
| **Hosted** | MCPServerHosted | Fully hosted MCP servers with remote endpoints |
| **Streamable HTTP** | MCPServerStreamableHttp | HTTP-based streaming MCP servers |
| **Server-Sent Events** | MCPServerSSE | SSE-based real-time MCP servers |
| **Standard I/O** | MCPServerStdio | Process-based MCP servers using stdio communication |

## Advanced Usage

### OpenAI Agents Integration

- **Agent Configuration**: Register MCP tools with existing OpenAI Agents SDK applications
- **Dynamic Tool Addition**: Runtime addition of MCP tool servers to active agents
- **Server Type Selection**: Choose appropriate MCP server types for different scenarios
- **Authentication Flow**: Seamless integration with Microsoft Agent 365 authentication

### MCP Tool Management

The service provides comprehensive MCP tool management capabilities:
- Automatic discovery of available MCP tool servers
- Registration with OpenAI Agents SDK framework
- Support for multiple concurrent MCP server types
- Runtime management of tool server configurations

## Architecture

The OpenAI tooling extensions follow a service-oriented architecture:

- **Registration Layer**: MCP tool registration and management services
- **OpenAI Integration Layer**: Native OpenAI Agents SDK integration and compatibility
- **Server Management Layer**: Multi-type MCP server support and configuration
- **Authentication Layer**: Microsoft Agent 365 authentication and authorization

## Integration with Microsoft Agent 365 SDK

This package works seamlessly with other Microsoft Agent 365 SDK components:

| Package | Integration |
|---------|-------------|
| `microsoft-agents-a365-tooling` | Core tooling utilities and MCP server configuration |
| `microsoft-agents-a365-runtime` | Runtime utilities and environment management |
| `microsoft-agents-a365-hosting-core` | Agent hosting and middleware services |
| `microsoft-agents-a365-observability-extensions-openai` | OpenAI observability and monitoring |

## Sample Applications

Check out these working examples:

| Sample | Description | Location |
|--------|-------------|----------|
| **OpenAI MCP Agent** | Basic OpenAI agent with MCP tool integration | `samples/openai-mcp-agent/` |
| **Multi-Tool OpenAI Agent** | Agent with multiple MCP server types | `samples/multi-tool-openai-agent/` |
| **Enterprise OpenAI Deployment** | Production-ready OpenAI agent deployment | `samples/enterprise-openai-deployment/` |

## Requirements

- **Python**: 3.11+
- **Dependencies**:
  - `microsoft-agents-a365-tooling >= 0.1.0`
  - `openai-agents`
  - `asyncio-throttle`

## Common Use Cases

### OpenAI Agents Development
- Register MCP tool servers with OpenAI Agents SDK applications
- Integrate with existing OpenAI agent workflows and frameworks
- Leverage Microsoft Agent 365 tooling infrastructure with OpenAI agents
- Deploy agents with comprehensive MCP tooling capabilities

### Enterprise OpenAI Deployment
- Manage MCP tool registration across multiple OpenAI environments
- Integrate with existing Microsoft Agent 365 infrastructure
- Support multi-tenant deployments with OpenAI Agents SDK
- Enable enterprise-scale agent deployments with OpenAI tooling

### Development and Testing
- Test MCP tool integration with OpenAI Agents SDK
- Validate agent configurations with various MCP server types
- Support development workflows with OpenAI tooling integration
- Enable debugging and monitoring with OpenAI observability

## Quick Links

📦 [All SDK Packages on PyPI](TODO: Update when packages are published)  
📖 [Complete Documentation](https://github.com/microsoft/Agent365/tree/main/python)  
💡 [Python Samples Repository](https://github.com/microsoft/Agent365/tree/main/samples)  
🐛 [Report Issues](https://github.com/microsoft/Agent365/issues)  
🤖 [OpenAI Agents Documentation](https://platform.openai.com/docs/assistants/overview)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.