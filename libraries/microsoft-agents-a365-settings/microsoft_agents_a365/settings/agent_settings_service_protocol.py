# Copyright (c) Microsoft. All rights reserved.

"""Service interface for managing agent settings."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from .models import AgentSettings, AgentSettingsTemplate


class AgentSettingsServiceProtocol(ABC):
    """Protocol for managing agent settings templates and agent instance settings."""

    @abstractmethod
    async def get_settings_template_by_agent_type(
        self,
        agent_type: str,
        auth_token: str,
    ) -> Optional[AgentSettingsTemplate]:
        """
        Get the settings template for the specified agent type.

        Args:
            agent_type: The type of agent to get the template for.
            auth_token: The authentication token for accessing the API.

        Returns:
            The settings template for the specified agent type, or None if not found.
        """

    @abstractmethod
    async def set_settings_template_by_agent_type(
        self,
        agent_type: str,
        template: AgentSettingsTemplate,
        auth_token: str,
    ) -> AgentSettingsTemplate:
        """
        Set or update the settings template for the specified agent type.

        Args:
            agent_type: The type of agent to set the template for.
            template: The settings template to set.
            auth_token: The authentication token for accessing the API.

        Returns:
            The updated settings template.
        """

    @abstractmethod
    async def get_settings_by_agent_instance(
        self,
        agent_instance_id: str,
        auth_token: str,
    ) -> Optional[AgentSettings]:
        """
        Get the settings for the specified agent instance.

        Args:
            agent_instance_id: The unique identifier of the agent instance.
            auth_token: The authentication token for accessing the API.

        Returns:
            The settings for the specified agent instance, or None if not found.
        """

    @abstractmethod
    async def set_settings_by_agent_instance(
        self,
        agent_instance_id: str,
        settings: AgentSettings,
        auth_token: str,
    ) -> AgentSettings:
        """
        Set or update the settings for the specified agent instance.

        Args:
            agent_instance_id: The unique identifier of the agent instance.
            settings: The settings to set.
            auth_token: The authentication token for accessing the API.

        Returns:
            The updated settings.
        """
