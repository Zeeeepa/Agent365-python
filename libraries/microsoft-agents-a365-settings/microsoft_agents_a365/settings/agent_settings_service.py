# Copyright (c) Microsoft. All rights reserved.

"""Service implementation for managing agent settings."""

from __future__ import annotations

import logging
import os
from typing import Optional
from urllib.parse import quote, urlparse

import httpx

from .agent_settings_service_protocol import AgentSettingsServiceProtocol
from .constants import DEFAULT_PLATFORM_BASE_URL, PLATFORM_ENDPOINT_CONFIG_KEY
from .models import AgentSettings, AgentSettingsTemplate

logger = logging.getLogger(__name__)


class AgentSettingsService(AgentSettingsServiceProtocol):
    """Provides services for managing agent settings templates and agent instance settings."""

    def __init__(
        self,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """
        Initialize a new instance of the AgentSettingsService.

        Args:
            http_client: Optional HTTP client for making API requests.
                         If not provided, a new client will be created.
        """
        self._http_client = http_client
        self._owns_client = http_client is None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create an HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client

    async def close(self) -> None:
        """Close the HTTP client if owned by this service."""
        if self._owns_client and self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    async def __aenter__(self) -> "AgentSettingsService":
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager."""
        await self.close()

    def _get_platform_base_url(self) -> str:
        """Get the platform base URL from configuration or use default."""
        configured_url = os.environ.get(PLATFORM_ENDPOINT_CONFIG_KEY)
        if configured_url:
            # Validate the configured URL is a valid URI
            try:
                parsed = urlparse(configured_url)
                if parsed.scheme in ("http", "https") and parsed.netloc:
                    return configured_url.rstrip("/")
            except Exception:
                pass
            logger.warning("Invalid platform URL configured: %s. Using default.", configured_url)
        return DEFAULT_PLATFORM_BASE_URL

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

        Raises:
            ValueError: If agent_type or auth_token is empty.
            RuntimeError: If the API request fails.
        """
        if not agent_type or not agent_type.strip():
            raise ValueError("Agent type cannot be null or empty.")

        if not auth_token or not auth_token.strip():
            raise ValueError("Auth token cannot be null or empty.")

        endpoint = (
            f"{self._get_platform_base_url()}/agents/types/"
            f"{quote(agent_type, safe='')}/settings/template"
        )
        logger.info("Getting settings template for agent type: %s", agent_type)

        try:
            client = await self._get_client()
            response = await client.get(
                endpoint,
                headers={"Authorization": f"Bearer {auth_token}"},
            )

            if response.status_code == 404:
                logger.info("Settings template not found for agent type: %s", agent_type)
                return None

            response.raise_for_status()
            return AgentSettingsTemplate.model_validate_json(response.content)

        except httpx.HTTPError as ex:
            logger.exception("Failed to get settings template for agent type: %s", agent_type)
            raise RuntimeError(
                f"Failed to get settings template for agent type '{agent_type}'."
            ) from ex

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

        Raises:
            ValueError: If agent_type or auth_token is empty, or template is None.
            RuntimeError: If the API request fails.
        """
        if not agent_type or not agent_type.strip():
            raise ValueError("Agent type cannot be null or empty.")

        if template is None:
            raise ValueError("Template cannot be None.")

        if not auth_token or not auth_token.strip():
            raise ValueError("Auth token cannot be null or empty.")

        endpoint = (
            f"{self._get_platform_base_url()}/agents/types/"
            f"{quote(agent_type, safe='')}/settings/template"
        )
        logger.info("Setting settings template for agent type: %s", agent_type)

        try:
            client = await self._get_client()
            response = await client.put(
                endpoint,
                headers={
                    "Authorization": f"Bearer {auth_token}",
                    "Content-Type": "application/json",
                },
                content=template.model_dump_json(by_alias=True),
            )

            response.raise_for_status()
            return AgentSettingsTemplate.model_validate_json(response.content)

        except httpx.HTTPError as ex:
            logger.exception("Failed to set settings template for agent type: %s", agent_type)
            raise RuntimeError(
                f"Failed to set settings template for agent type '{agent_type}'."
            ) from ex

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

        Raises:
            ValueError: If agent_instance_id or auth_token is empty.
            RuntimeError: If the API request fails.
        """
        if not agent_instance_id or not agent_instance_id.strip():
            raise ValueError("Agent instance ID cannot be null or empty.")

        if not auth_token or not auth_token.strip():
            raise ValueError("Auth token cannot be null or empty.")

        endpoint = (
            f"{self._get_platform_base_url()}/agents/"
            f"{quote(agent_instance_id, safe='')}/settings"
        )
        logger.info("Getting settings for agent instance: %s", agent_instance_id)

        try:
            client = await self._get_client()
            response = await client.get(
                endpoint,
                headers={"Authorization": f"Bearer {auth_token}"},
            )

            if response.status_code == 404:
                logger.info("Settings not found for agent instance: %s", agent_instance_id)
                return None

            response.raise_for_status()
            return AgentSettings.model_validate_json(response.content)

        except httpx.HTTPError as ex:
            logger.exception("Failed to get settings for agent instance: %s", agent_instance_id)
            raise RuntimeError(
                f"Failed to get settings for agent instance '{agent_instance_id}'."
            ) from ex

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

        Raises:
            ValueError: If agent_instance_id or auth_token is empty, or settings is None.
            RuntimeError: If the API request fails.
        """
        if not agent_instance_id or not agent_instance_id.strip():
            raise ValueError("Agent instance ID cannot be null or empty.")

        if settings is None:
            raise ValueError("Settings cannot be None.")

        if not auth_token or not auth_token.strip():
            raise ValueError("Auth token cannot be null or empty.")

        endpoint = (
            f"{self._get_platform_base_url()}/agents/"
            f"{quote(agent_instance_id, safe='')}/settings"
        )
        logger.info("Setting settings for agent instance: %s", agent_instance_id)

        try:
            client = await self._get_client()
            response = await client.put(
                endpoint,
                headers={
                    "Authorization": f"Bearer {auth_token}",
                    "Content-Type": "application/json",
                },
                content=settings.model_dump_json(by_alias=True),
            )

            response.raise_for_status()
            return AgentSettings.model_validate_json(response.content)

        except httpx.HTTPError as ex:
            logger.exception("Failed to set settings for agent instance: %s", agent_instance_id)
            raise RuntimeError(
                f"Failed to set settings for agent instance '{agent_instance_id}'."
            ) from ex
