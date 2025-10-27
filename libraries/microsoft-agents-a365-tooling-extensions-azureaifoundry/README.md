# Microsoft Agent 365 Tooling Extensions - Azure AI Foundry
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-azureaifoundry.svg)](https://badge.fury.io/py/microsoft-agents-a365-tooling-extensions-azureaifoundry)

Azure AI Foundry integration tools and MCP tool registration services for AI agent applications built with the Microsoft Agent 365 SDK. Provides specialized tooling for integrating MCP (Model Context Protocol) servers with Azure AI Foundry agents and projects.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The Azure AI Foundry tooling extensions specifically provide integration with Azure AI Foundry (Azure AI Projects and Agents), enabling seamless registration and management of MCP tool servers within the Azure AI ecosystem.

## Key Features

✅ **Azure AI Foundry Integration** - Native integration with Azure AI Projects and Agents  
✅ **MCP Tool Registration** - Automatic registration of MCP servers with Azure AI Foundry agents  
✅ **Azure Identity Support** - Built-in Azure authentication with DefaultAzureCredential  
✅ **Tool Resource Management** - Comprehensive management of tool definitions and resources  
✅ **Multi-Environment Support** - Support for development and production deployment scenarios  
✅ **Enterprise Ready** - Production-grade tooling for Azure-based agent deployments  

## Installation

```bash
pip install microsoft-agents-a365-tooling-extensions-azureaifoundry
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 Azure AI Foundry Tooling Extensions enable seamless integration between MCP tool servers and Azure AI Foundry agents. Key concepts include:

- **MCP Tool Registration**: Automatic registration of MCP servers with Azure AI Foundry agents
- **Azure AI Projects Integration**: Native integration with Azure AI Projects and project clients
- **Tool Resource Management**: Management of tool definitions, resources, and configurations
- **Azure Identity Integration**: Seamless authentication using Azure DefaultAzureCredential

### Getting Started

1. Install the package: `pip install microsoft-agents-a365-tooling-extensions-azureaifoundry`
2. Configure Azure credentials and project settings
3. Use the MCP tool registration service to add tools to your agents
4. Deploy and manage your Azure AI Foundry agents with MCP capabilities

### Basic Usage

```python
from microsoft_agents_a365.tooling.extensions.azureaifoundry import McpToolRegistrationService
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Create Azure AI Project client
credential = DefaultAzureCredential()
project_client = AIProjectClient(
    credential=credential,
    endpoint="your-project-endpoint",
    subscription_id="your-subscription-id",
    resource_group_name="your-resource-group",
    project_name="your-project-name"
)

# Create MCP tool registration service
registration_service = McpToolRegistrationService()

# Add MCP tool servers to your Azure AI Foundry agent
await registration_service.add_tool_servers_to_agent(
    project_client=project_client,
    agent_id="your-agent-id",
    environment_id="prod",
    auth_token="your-auth-token"
)
```

## Core Azure AI Foundry Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **McpToolRegistrationService** | Tool Registration | Register MCP servers with Azure AI Foundry agents |
| **Azure Identity Integration** | Authentication | Seamless Azure authentication and credential management |
| **Tool Resource Management** | Resource Management | Manage tool definitions and resources in Azure AI Foundry |
| **Project Client Integration** | Azure Integration | Native integration with Azure AI Projects and clients |

## Supported Azure AI Foundry Features

| Feature | Component | Description |
|---------|-----------|-------------|
| **Agent Tool Registration** | MCP server integration | Add MCP tool servers to Azure AI Foundry agents |
| **Azure Authentication** | Identity management | Azure DefaultAzureCredential integration |
| **Project Integration** | Azure AI Projects | Native integration with Azure AI project clients |
| **Resource Management** | Tool resources | Manage tool definitions and configurations |

## Advanced Usage

### Azure AI Foundry Integration

- **Agent Configuration**: Register MCP tools with existing Azure AI Foundry agents
- **Project Management**: Integration with Azure AI Projects for centralized management
- **Resource Allocation**: Automatic tool resource allocation and configuration
- **Environment Management**: Support for multiple deployment environments

### MCP Tool Registration

The service provides comprehensive MCP tool registration capabilities:
- Automatic discovery of available MCP tool servers
- Registration with Azure AI Foundry agent infrastructure
- Tool resource management and configuration
- Support for both development and production scenarios

## Architecture

The Azure AI Foundry extensions follow a service-oriented architecture:

- **Registration Layer**: MCP tool registration and management services
- **Azure Integration Layer**: Native Azure AI Foundry and identity integration
- **Resource Management Layer**: Tool definition and resource management
- **Configuration Layer**: Environment-specific configuration and settings

## Integration with Microsoft Agent 365 SDK

This package works seamlessly with other Microsoft Agent 365 SDK components:

| Package | Integration |
|---------|-------------|
| `microsoft-agents-a365-tooling` | Core tooling utilities and MCP server configuration |
| `microsoft-agents-a365-runtime` | Runtime utilities and environment management |
| `microsoft-agents-a365-observability-core` | Observability and monitoring for Azure deployments |
| `microsoft-agents-a365-hosting-core` | Agent hosting and middleware services |

## Sample Applications

Check out these working examples:

| Sample | Description | Location |
|--------|-------------|----------|
| **Azure AI Foundry Agent** | Basic agent with MCP tool integration | `samples/azure-foundry-agent/` |
| **Multi-Tool Agent** | Agent with multiple MCP tool servers | `samples/multi-tool-azure-agent/` |
| **Enterprise Azure Deployment** | Production-ready Azure AI Foundry deployment | `samples/enterprise-azure-deployment/` |

## Requirements

- **Python**: 3.11+
- **Dependencies**:
  - `microsoft-agents-a365-tooling >= 0.1.0`
  - `azure-ai-projects >= 1.0.0`
  - `azure-ai-agents >= 1.1.0b4`
  - `azure-identity >= 1.12.0`

## Common Use Cases

### Azure AI Foundry Development
- Register MCP tool servers with Azure AI Foundry agents
- Integrate with Azure AI Projects for centralized agent management
- Leverage Azure identity for secure authentication and authorization
- Deploy agents with comprehensive tooling capabilities

### Enterprise Azure Deployment
- Manage MCP tool registration across multiple Azure environments
- Integrate with existing Azure infrastructure and identity systems
- Support multi-tenant deployments with Azure AI Foundry
- Enable enterprise-scale agent deployments with Azure tooling

### Development and Testing
- Test MCP tool integration in Azure AI Foundry environments
- Validate agent configurations with Azure AI Projects
- Support development workflows with Azure tooling integration
- Enable debugging and monitoring with Azure observability

## Quick Links

📦 [All SDK Packages on PyPI](TODO: Update when packages are published)  
📖 [Complete Documentation](https://github.com/microsoft/Agent365/tree/main/python)  
💡 [Python Samples Repository](https://github.com/microsoft/Agent365/tree/main/samples)  
🐛 [Report Issues](https://github.com/microsoft/Agent365/issues)  
☁️ [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.