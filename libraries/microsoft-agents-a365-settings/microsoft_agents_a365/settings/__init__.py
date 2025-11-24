# Copyright (c) Microsoft. All rights reserved.

"""
Microsoft Agent 365 Settings SDK.

This module provides functionality to manage Agent 365 settings templates
and agent instance settings.
"""

from .agent_settings_service import AgentSettingsService
from .agent_settings_service_protocol import AgentSettingsServiceProtocol
from .constants import (
    DEFAULT_PLATFORM_AUTH_SCOPE,
    DEFAULT_PLATFORM_BASE_URL,
    PLATFORM_AUTH_SCOPE_CONFIG_KEY,
    PLATFORM_ENDPOINT_CONFIG_KEY,
)
from .models import AgentSettingProperty, AgentSettings, AgentSettingsTemplate

__all__ = [
    # Models
    "AgentSettingProperty",
    "AgentSettings",
    "AgentSettingsTemplate",
    # Service
    "AgentSettingsService",
    "AgentSettingsServiceProtocol",
    # Constants
    "DEFAULT_PLATFORM_BASE_URL",
    "PLATFORM_ENDPOINT_CONFIG_KEY",
    "PLATFORM_AUTH_SCOPE_CONFIG_KEY",
    "DEFAULT_PLATFORM_AUTH_SCOPE",
]
