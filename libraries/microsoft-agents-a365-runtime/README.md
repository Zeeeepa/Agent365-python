# Microsoft Agent 365 Runtime
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-runtime.svg)](https://badge.fury.io/py/microsoft-agents-a365-runtime)

Core runtime utilities and environment management for AI agent applications built with the Microsoft Agent 365 SDK. Provides essential Power Platform API discovery, environment configuration, and version management for enterprise-grade conversational AI agents.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The runtime package provides core utilities for environment management, Power Platform API discovery, and version handling that enable agents to operate seamlessly across different deployment environments.

## Key Features

✅ **Power Platform API Discovery** - Automatic discovery of Power Platform API endpoints across environments  
✅ **Environment Management** - Intelligent environment detection and configuration utilities  
✅ **Authentication Scopes** - Environment-specific authentication scope resolution  
✅ **Version Management** - Automated version generation and SDK version handling  
✅ **Multi-Environment Support** - Support for development, test, preprod, and production environments  
✅ **Enterprise Ready** - Production-grade utilities for large-scale deployments  

## Installation

```bash
pip install microsoft-agents-a365-runtime
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 Runtime provides essential utilities for agent applications to operate across different environments. Key concepts include:

- **Environment Detection**: Automatic detection of current deployment environment
- **API Discovery**: Dynamic discovery of Power Platform API endpoints
- **Authentication Scopes**: Environment-specific authentication scope resolution
- **Version Management**: Automated version generation for SDK packages

### Getting Started

1. Install the package: `pip install microsoft-agents-a365-runtime`
2. Import the runtime utilities in your agent application
3. Use environment detection and API discovery for configuration
4. Leverage version utilities for package management

### Basic Usage

```python
from microsoft_agents_a365.runtime import (
    get_observability_authentication_scope,
    PowerPlatformApiDiscovery,
    ClusterCategory
)

# Get authentication scope for current environment
auth_scope = get_observability_authentication_scope()

# Discover Power Platform API endpoints
discovery = PowerPlatformApiDiscovery("prod")
token_audience = discovery.get_token_audience()
tenant_endpoint = discovery.get_tenant_endpoint("your-tenant-id")
```

## Core Runtime Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **Environment Utils** | Environment Detection | Detect current environment and get appropriate configuration |
| **Power Platform API Discovery** | API Endpoint Resolution | Discover Power Platform API endpoints for different environments |
| **Version Utils** | Version Management | Generate and manage SDK package versions |
| **Cluster Categories** | Environment Classification | Support for multiple deployment cluster categories |

## Supported Environments

| Environment | Cluster Category | Authentication Scope |
|-------------|------------------|---------------------|
| **Development** | `preprod` | `https://api.preprod.powerplatform.com/.default` |
| **Test** | `test` | `https://api.test.powerplatform.com/.default` |
| **Production** | `prod` | `https://api.powerplatform.com/.default` |
| **Government** | `gov` | Government cloud endpoints |
| **Sovereign Clouds** | `mooncake`, `dod`, etc. | Region-specific endpoints |

## Advanced Usage

### API Discovery Features

- **Tenant Endpoint Resolution**: Generate tenant-specific API endpoints
- **Island Cluster Support**: Support for tenant island cluster endpoints
- **Multi-Cloud Support**: Support for sovereign and government clouds
- **Dynamic Configuration**: Runtime configuration based on environment detection

### Environment Configuration

The runtime automatically detects environments through:
- Environment variable detection (`PYTHON_ENVIRONMENT`)
- Automatic environment classification
- Fallback to production configuration for unknown environments
- Support for custom environment configurations

## Architecture

The runtime follows a utility-focused architecture:

- **Environment Layer**: Environment detection and configuration management
- **Discovery Layer**: Power Platform API endpoint discovery and resolution
- **Version Layer**: SDK version management and generation utilities
- **Configuration Layer**: Environment-specific configuration resolution

## Integration with Microsoft Agent 365 SDK

This package works seamlessly with other Microsoft Agent 365 SDK components:

| Package | Integration |
|---------|-------------|
| `microsoft-agents-a365-observability-core` | Provides authentication scopes for observability services |
| `microsoft-agents-a365-tooling` | Environment detection for tool configuration |
| `microsoft-agents-a365-hosting-core` | Runtime environment configuration for hosting |
| `microsoft-agents-a365-notifications` | Environment-aware notification routing |

## Sample Applications

Check out these working examples:

| Sample | Description | Location |
|--------|-------------|----------|
| **Multi-Environment Agent** | Agent that adapts to different environments | `samples/multi-env-agent/` |
| **Power Platform Integration** | Agent with Power Platform API discovery | `samples/power-platform-agent/` |
| **Enterprise Deployment** | Production-ready agent with environment management | `samples/enterprise-deployment/` |

## Requirements

- **Python**: 3.11+
- **Dependencies**: 
  - No external dependencies (lightweight core utilities)

## Common Use Cases

### Development and Testing
- Automatically configure agents for different development environments
- Discover appropriate API endpoints for testing scenarios
- Manage version generation during development cycles
- Support local development with preprod configurations

### Production Deployment
- Automatically detect production environments and configure accordingly
- Resolve correct Power Platform API endpoints for production workloads
- Generate appropriate version strings for release packages
- Support multi-tenant deployments with tenant-specific endpoints

### Enterprise Integration
- Support sovereign cloud deployments (Government, DoD, etc.)
- Integrate with existing enterprise environment management
- Provide consistent configuration across multiple deployment environments
- Enable environment-aware authentication and API access

## Quick Links

📦 [All SDK Packages on PyPI](TODO: Update when packages are published)  
📖 [Complete Documentation](https://github.com/microsoft/Agent365/tree/main/python)  
💡 [Python Samples Repository](https://github.com/microsoft/Agent365/tree/main/samples)  
🐛 [Report Issues](https://github.com/microsoft/Agent365/issues)  
🏢 [Power Platform Documentation](https://docs.microsoft.com/power-platform/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.