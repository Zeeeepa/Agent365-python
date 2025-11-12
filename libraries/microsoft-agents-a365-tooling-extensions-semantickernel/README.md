# Microsoft Agent 365 Tooling Extensions - Semantic Kernel
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-semantickernel.svg)](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-semantickernel)

Microsoft Semantic Kernel integration tools and MCP tool registration services for AI agent applications built with the Microsoft Agent 365 SDK. Provides specialized tooling for integrating MCP (Model Context Protocol) servers with Semantic Kernel-based agent applications.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The Semantic Kernel tooling extensions specifically provide integration with the Microsoft Semantic Kernel framework, enabling seamless registration and management of MCP tool servers within Semantic Kernel-based agent applications.

## Key Features

✅ **Semantic Kernel Integration** - Native integration with Microsoft Semantic Kernel framework  
✅ **MCP Tool Registration** - Automatic registration of MCP servers with Semantic Kernel agents  
✅ **Plugin Management** - Seamless integration with Semantic Kernel's plugin architecture  
✅ **Streamable HTTP Support** - Built-in support for MCP streamable HTTP plugins  
✅ **Kernel Function Integration** - Integration with Semantic Kernel's function calling system  
✅ **Enterprise Ready** - Production-grade tooling for Semantic Kernel-based agent deployments  

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-semantickernel
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 Semantic Kernel Tooling Extensions enable seamless integration between MCP tool servers and Semantic Kernel applications. Key concepts include:

- **MCP Tool Registration**: Automatic registration of MCP servers with Semantic Kernel agents
- **Semantic Kernel Integration**: Native integration with Semantic Kernel framework and plugins
- **Plugin Architecture**: Leverage Semantic Kernel's plugin system for MCP server integration
- **Kernel Function Support**: Integration with Semantic Kernel's function calling capabilities

### Getting Started

1. Install the package: `pip install microsoft-agents-a365-tooling-extensions-semantickernel`
2. Configure your Semantic Kernel application with MCP support
3. Use the MCP tool registration service to add tools to your kernel
4. Deploy and manage your Semantic Kernel agents with MCP capabilities

### Basic Usage

```python
from microsoft_agents_a365.tooling.extensions.semantickernel import McpToolRegistrationService
from semantic_kernel import Kernel

# Create Semantic Kernel instance
kernel = Kernel()

# Create MCP tool registration service
registration_service = McpToolRegistrationService()

# Add MCP tool servers to your Semantic Kernel
await registration_service.add_tool_servers_to_kernel(
    kernel=kernel,
    agentic_app_id="user-123",
    auth_token="your-auth-token"
)
```

## Core Semantic Kernel Integration Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **McpToolRegistrationService** | Tool Registration | Register MCP servers with Semantic Kernel applications |
| **MCPStreamableHttpPlugin** | Plugin Integration | Semantic Kernel plugin for MCP streamable HTTP servers |
| **Kernel Function Support** | Function Integration | Integration with Semantic Kernel's function calling system |
| **Configuration Management** | Setup Management | Configuration and setup of MCP tools within Semantic Kernel |

## Supported Semantic Kernel Features

| Feature | Component | Description |
|---------|-----------|-------------|
| **Plugin Architecture** | MCP plugin integration | Leverage Semantic Kernel's plugin system for MCP servers |
| **Function Calling** | Kernel functions | Integration with Semantic Kernel's function calling capabilities |
| **Streamable HTTP** | MCPStreamableHttpPlugin | Support for MCP streamable HTTP server integration |
| **Tool Registration** | Dynamic registration | Runtime registration of MCP tools with Semantic Kernel |

## Advanced Usage

### Semantic Kernel Integration

- **Plugin Registration**: Register MCP tools as Semantic Kernel plugins
- **Kernel Function Integration**: Seamless integration with Semantic Kernel's function system
- **Dynamic Tool Addition**: Runtime addition of MCP tool servers to active kernels
- **Configuration Management**: Centralized configuration of MCP tools within Semantic Kernel

### MCP Tool Management

The service provides comprehensive MCP tool management capabilities:
- Automatic discovery of available MCP tool servers
- Registration with Semantic Kernel's plugin architecture
- Integration with Semantic Kernel's function calling system
- Support for streamable HTTP MCP server types

## Architecture

The Semantic Kernel tooling extensions follow a plugin-oriented architecture:

- **Registration Layer**: MCP tool registration and management services
- **Semantic Kernel Integration Layer**: Native Semantic Kernel framework integration
- **Plugin Management Layer**: Semantic Kernel plugin system integration
- **Function Integration Layer**: Kernel function calling system support

## Integration with Microsoft Agent 365 SDK

This package works seamlessly with other Microsoft Agent 365 SDK components:

| Package | Integration |
|---------|-------------|
| `microsoft-agents-a365-tooling` | Core tooling utilities and MCP server configuration |
| `microsoft-agents-a365-runtime` | Runtime utilities and environment management |
| `microsoft-agents-a365-observability-extensions-semantickernel` | Semantic Kernel observability and monitoring |
| `microsoft-agents-a365-hosting-core` | Agent hosting and middleware services |

## Sample Applications

Check out these working examples:

| Sample | Description | Location |
|--------|-------------|----------|
| **Semantic Kernel MCP Agent** | Basic Semantic Kernel agent with MCP tools | `samples/semantic-kernel-mcp-agent/` |
| **Multi-Plugin SK Agent** | Agent with multiple MCP plugins | `samples/multi-plugin-sk-agent/` |
| **Enterprise SK Deployment** | Production-ready Semantic Kernel deployment | `samples/enterprise-sk-deployment/` |

## Requirements

- **Python**: 3.11+
- **Dependencies**:
  - `microsoft-agents-a365-tooling >= 0.1.0`
  - `semantic-kernel >= 1.0.0`
  - `aiohttp >= 3.8.0`

## Common Use Cases

### Semantic Kernel Development
- Register MCP tool servers with Semantic Kernel applications
- Integrate with existing Semantic Kernel workflows and plugins
- Leverage Microsoft Agent 365 tooling infrastructure with Semantic Kernel
- Deploy agents with comprehensive MCP tooling capabilities

### Enterprise Semantic Kernel Deployment
- Manage MCP tool registration across multiple Semantic Kernel environments
- Integrate with existing Microsoft Agent 365 infrastructure
- Support multi-tenant deployments with Semantic Kernel framework
- Enable enterprise-scale agent deployments with Semantic Kernel tooling

### Development and Testing
- Test MCP tool integration with Semantic Kernel framework
- Validate agent configurations with Semantic Kernel plugins
- Support development workflows with Semantic Kernel tooling integration
- Enable debugging and monitoring with Semantic Kernel observability

## Quick Links

📦 [All SDK Packages on PyPI](TODO: Update when packages are published)  
📖 [Complete Documentation](https://github.com/microsoft/Agent365/tree/main/python)  
💡 [Python Samples Repository](https://github.com/microsoft/Agent365/tree/main/samples)  
🐛 [Report Issues](https://github.com/microsoft/Agent365/issues)  
🧠 [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.