# Microsoft Agent 365 Tooling
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-tooling.svg)](https://badge.fury.io/py/microsoft-agents-a365-tooling)

Cross-framework utilities and shared components for AI agent tooling built with the Microsoft Agent 365 SDK. Provides core tooling functionality including MCP (Model Context Protocol) server configuration, utilities, and services shared across different AI frameworks.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The tooling package provides core utilities, configuration management, and services that are shared across different AI framework integrations, enabling consistent tooling experiences across the entire SDK ecosystem.

## Key Features

✅ **MCP Server Configuration** - Comprehensive Model Context Protocol server configuration management  
✅ **Cross-Framework Utilities** - Shared utilities that work across different AI frameworks  
✅ **Tooling Gateway Integration** - Built-in integration with Microsoft Agent 365 tooling gateway  
✅ **Configuration Services** - Centralized configuration management for MCP tool servers  
✅ **URL Generation** - Automatic MCP server URL generation and endpoint management  
✅ **Enterprise Ready** - Production-grade tooling infrastructure for large-scale deployments  

## Installation

```bash
pip install microsoft-agents-a365-tooling
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 Tooling package provides foundational utilities for managing and configuring AI agent tooling. Key concepts include:

- **MCP Server Configuration**: Structured configuration for Model Context Protocol servers
- **Tooling Gateway**: Centralized gateway for managing agent tools and services
- **Configuration Services**: Services for managing and retrieving tool configurations
- **Cross-Framework Compatibility**: Utilities that work across different AI frameworks

### Getting Started

1. Install the package: `pip install microsoft-agents-a365-tooling`
2. Import the tooling utilities in your agent application
3. Configure MCP servers and tooling gateway integration
4. Use shared utilities across your AI framework implementations

### Basic Usage

```python
from microsoft_agents_a365.tooling import (
    MCPServerConfig,
    McpToolServerConfigurationService,
    build_mcp_server_url
)

# Configure MCP server
mcp_config = MCPServerConfig(
    mcp_server_name="my-tool-server",
    mcp_server_unique_name="my-unique-server-id"
)

# Use configuration service to list available MCP servers
config_service = McpToolServerConfigurationService()
mcp_servers = await config_service.list_tool_servers(
    agentic_app_id="agent-123",
    environment_id="prod",
    auth_token="your-auth-token"
)
```

## Core Tooling Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **MCPServerConfig** | Configuration Model | Structured configuration for MCP server instances |
| **McpToolServerConfigurationService** | Configuration Service | Service for managing MCP tool server configurations |
| **Utility Functions** | Helper Functions | URL generation, gateway resolution, and common utilities |
| **Constants** | Configuration Constants | Shared constants used across tooling components |

## Supported Tooling Features

| Feature | Component | Description |
|---------|-----------|-------------|
| **MCP Server Management** | Configuration and URL generation | Manage Model Context Protocol server configurations |
| **Tooling Gateway** | Gateway integration utilities | Connect to Microsoft Agent 365 tooling gateway |
| **Cross-Framework Support** | Shared utilities | Common functionality across AI frameworks |
| **Configuration Management** | Centralized configuration | Manage tool configurations and settings |

## Advanced Usage

### MCP Server Configuration

- **Server Registration**: Register and configure MCP servers with unique identifiers
- **URL Generation**: Automatic generation of MCP server endpoints and URLs
- **Configuration Validation**: Built-in validation for server configuration parameters
- **Service Discovery**: Discover and connect to configured MCP servers

### Tooling Gateway Integration

The tooling package provides seamless integration with the Microsoft Agent 365 tooling gateway:
- Digital worker endpoint resolution
- MCP base URL configuration
- Gateway service discovery
- Cross-framework tool coordination

## Architecture

The tooling package follows a service-oriented architecture:

- **Models Layer**: Data models for configuration and server definitions
- **Services Layer**: Configuration services and management functionality
- **Utils Layer**: Shared utilities and helper functions
- **Integration Layer**: Cross-framework compatibility and gateway integration

## Integration with Microsoft Agent 365 SDK

This package works seamlessly with other Microsoft Agent 365 SDK components:

| Package | Integration |
|---------|-------------|
| `microsoft-agents-a365-tooling-extensions-azureaifoundry` | Azure AI Foundry-specific tooling extensions |
| `microsoft-agents-a365-tooling-extensions-openai` | OpenAI-specific tooling integrations |
| `microsoft-agents-a365-tooling-extensions-semantickernel` | Semantic Kernel tooling extensions |
| `microsoft-agents-a365-runtime` | Runtime utilities and environment management |

## Sample Applications

Check out these working examples:

| Sample | Description | Location |
|--------|-------------|----------|
| **MCP Server Setup** | Basic MCP server configuration and management | `samples/mcp-server-setup/` |
| **Multi-Framework Tooling** | Tooling utilities across different AI frameworks | `samples/multi-framework-tooling/` |
| **Gateway Integration** | Integration with Microsoft Agent 365 tooling gateway | `samples/gateway-integration/` |

## Requirements

- **Python**: 3.11+
- **Dependencies**:
  - `pydantic >= 2.0.0`
  - `typing-extensions >= 4.0.0`

## Common Use Cases

### Framework Integration
- Configure MCP servers for different AI frameworks
- Manage tool configurations across multiple framework implementations
- Provide consistent tooling experiences across AI frameworks
- Enable cross-framework tool sharing and coordination

### Enterprise Deployment
- Centralize tool configuration management across multiple agents
- Integrate with existing enterprise tooling infrastructure
- Manage MCP server deployments at scale
- Support multi-tenant tooling configurations

### Development and Testing
- Provide shared utilities for development across different frameworks
- Enable consistent configuration patterns across development teams
- Support testing with standardized tool configurations
- Facilitate debugging with unified tooling utilities

## Quick Links

📦 [All SDK Packages on PyPI](TODO: Update when packages are published)  
📖 [Complete Documentation](https://github.com/microsoft/Agent365/tree/main/python)  
💡 [Python Samples Repository](https://github.com/microsoft/Agent365/tree/main/samples)  
🐛 [Report Issues](https://github.com/microsoft/Agent365/issues)  
🔧 [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.