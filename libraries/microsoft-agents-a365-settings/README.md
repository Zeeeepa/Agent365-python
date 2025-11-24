# Microsoft Agent 365 Settings SDK

This package provides functionality to manage Agent 365 settings templates and agent instance settings.

## Overview

The Settings SDK enables developers to:

- **Get or Set Agent Setting Templates by Agent Type**: Configure default settings templates that apply to specific types of agents.
- **Get or Set Agent Settings by Agent Instance**: Configure settings for individual agent instances.

## Installation

```bash
pip install microsoft-agents-a365-settings
```

## Usage

### Creating the Service

```python
from microsoft_agents_a365.settings import AgentSettingsService

# Create a service instance
async with AgentSettingsService() as service:
    # Use the service
    ...

# Or manage lifecycle manually
service = AgentSettingsService()
try:
    # Use the service
    ...
finally:
    await service.close()
```

### Getting Settings Template by Agent Type

```python
from microsoft_agents_a365.settings import AgentSettingsService

async def get_template(agent_type: str, auth_token: str):
    async with AgentSettingsService() as service:
        template = await service.get_settings_template_by_agent_type(
            agent_type=agent_type,
            auth_token=auth_token,
        )
        return template
```

### Setting a Settings Template

```python
from microsoft_agents_a365.settings import (
    AgentSettingsService,
    AgentSettingsTemplate,
    AgentSettingProperty,
)

async def set_template(agent_type: str, auth_token: str):
    template = AgentSettingsTemplate(
        agent_type=agent_type,
        name="Custom Agent Template",
        properties=[
            AgentSettingProperty(
                name="maxRetries",
                value="3",
                type="integer",
                required=True,
                description="Maximum number of retry attempts",
            )
        ],
    )
    
    async with AgentSettingsService() as service:
        result = await service.set_settings_template_by_agent_type(
            agent_type=agent_type,
            template=template,
            auth_token=auth_token,
        )
        return result
```

### Getting Settings by Agent Instance

```python
from microsoft_agents_a365.settings import AgentSettingsService

async def get_settings(agent_instance_id: str, auth_token: str):
    async with AgentSettingsService() as service:
        settings = await service.get_settings_by_agent_instance(
            agent_instance_id=agent_instance_id,
            auth_token=auth_token,
        )
        if settings:
            for prop in settings.properties:
                print(f"{prop.name}: {prop.value}")
        return settings
```

### Setting Agent Instance Settings

```python
from microsoft_agents_a365.settings import (
    AgentSettingsService,
    AgentSettings,
    AgentSettingProperty,
)

async def set_settings(agent_instance_id: str, auth_token: str):
    settings = AgentSettings(
        agent_instance_id=agent_instance_id,
        agent_type="custom-agent",
        properties=[
            AgentSettingProperty(
                name="apiEndpoint",
                value="https://api.example.com",
                type="string",
            )
        ],
    )
    
    async with AgentSettingsService() as service:
        result = await service.set_settings_by_agent_instance(
            agent_instance_id=agent_instance_id,
            settings=settings,
            auth_token=auth_token,
        )
        return result
```

## Configuration

The service uses the following environment variables for configuration:

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `MCP_PLATFORM_ENDPOINT` | Override the base URL for the Agent 365 platform | `https://agent365.svc.cloud.microsoft` |
| `MCP_PLATFORM_AUTHENTICATION_SCOPE` | The authentication scope for the platform | `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1/.default` |

## Models

### AgentSettingsTemplate

Represents a settings template for a specific agent type.

| Property | Type | Description |
|----------|------|-------------|
| `id` | str | Unique identifier of the template |
| `agent_type` | str | The agent type this template applies to |
| `name` | str | Display name of the template |
| `description` | str \| None | Optional description |
| `version` | str | Template version (default: "1.0") |
| `properties` | list[AgentSettingProperty] | Collection of setting properties |

### AgentSettings

Represents settings for a specific agent instance.

| Property | Type | Description |
|----------|------|-------------|
| `id` | str | Unique identifier of the settings |
| `agent_instance_id` | str | The agent instance these settings belong to |
| `template_id` | str \| None | Optional reference to the template |
| `agent_type` | str | The agent type |
| `properties` | list[AgentSettingProperty] | Collection of setting values |
| `created_at` | datetime | Creation timestamp |
| `modified_at` | datetime | Last modification timestamp |

### AgentSettingProperty

Represents a single setting property.

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Name of the setting |
| `value` | str | Current value |
| `type` | str | Value type (default: "string") |
| `required` | bool | Whether the setting is required |
| `description` | str \| None | Optional description |
| `default_value` | str \| None | Optional default value |

## License

This project is licensed under the MIT License.
