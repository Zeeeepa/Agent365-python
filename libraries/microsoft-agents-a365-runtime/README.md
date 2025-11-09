# microsoft-agents-a365-runtime

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-runtime?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-runtime)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-runtime?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-runtime)

Core runtime utilities and environment management for AI agent applications. This package provides essential Power Platform API discovery, environment configuration, and authentication scope resolution.

## Installation

```bash
pip install microsoft-agents-a365-runtime
```

## Usage

### Power Platform API Discovery

```python
from microsoft_agents_a365.runtime import (
    PowerPlatformApiDiscovery,
    ClusterCategory
)

# Initialize API discovery for preprod environment
api_discovery = PowerPlatformApiDiscovery(ClusterCategory.PREPROD)

# Discover API endpoint for an environment
endpoint = api_discovery.discover_api(environment_id="env-123")
print(f"API Endpoint: {endpoint}")
```

### Get Authentication Scope

```python
from microsoft_agents_a365.runtime import get_observability_authentication_scope

# Get authentication scope for observability services
scope = get_observability_authentication_scope(environment_id="env-123")
print(f"Auth Scope: {scope}")
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
