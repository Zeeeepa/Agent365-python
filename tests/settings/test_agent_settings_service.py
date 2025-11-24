# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for AgentSettingsService."""

import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from microsoft_agents_a365.settings import (
    AgentSettings,
    AgentSettingsService,
    AgentSettingsTemplate,
)


class TestAgentSettingsServiceValidation(unittest.TestCase):
    """Test cases for AgentSettingsService validation logic."""

    def test_get_platform_base_url_default(self):
        """Test that default URL is used when no env var is set."""
        service = AgentSettingsService()
        with patch.dict(os.environ, {}, clear=True):
            url = service._get_platform_base_url()
            self.assertEqual(url, "https://agent365.svc.cloud.microsoft")

    def test_get_platform_base_url_from_env(self):
        """Test that URL from environment variable is used."""
        service = AgentSettingsService()
        with patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": "https://custom.endpoint.com"}):
            url = service._get_platform_base_url()
            self.assertEqual(url, "https://custom.endpoint.com")

    def test_get_platform_base_url_strips_trailing_slash(self):
        """Test that trailing slash is stripped from URL."""
        service = AgentSettingsService()
        with patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": "https://custom.endpoint.com/"}):
            url = service._get_platform_base_url()
            self.assertEqual(url, "https://custom.endpoint.com")

    def test_get_platform_base_url_invalid_uses_default(self):
        """Test that invalid URL falls back to default."""
        service = AgentSettingsService()
        with patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": "not-a-valid-url"}):
            url = service._get_platform_base_url()
            self.assertEqual(url, "https://agent365.svc.cloud.microsoft")


@pytest.mark.asyncio
class TestAgentSettingsServiceAsync:
    """Async test cases for AgentSettingsService."""

    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    async def test_get_settings_template_by_agent_type_success(self, mock_http_client):
        """Test getting settings template returns template on success."""
        expected_template = AgentSettingsTemplate(
            id="template-123",
            agent_type="custom-agent",
            name="Test Template",
            version="1.0",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = expected_template.model_dump_json(by_alias=True).encode()
        mock_response.raise_for_status = MagicMock()
        mock_http_client.get = AsyncMock(return_value=mock_response)

        service = AgentSettingsService(http_client=mock_http_client)
        result = await service.get_settings_template_by_agent_type("custom-agent", "test-token")

        assert result is not None
        assert result.id == "template-123"
        assert result.agent_type == "custom-agent"
        assert result.name == "Test Template"

    async def test_get_settings_template_by_agent_type_not_found(self, mock_http_client):
        """Test getting settings template returns None on 404."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_http_client.get = AsyncMock(return_value=mock_response)

        service = AgentSettingsService(http_client=mock_http_client)
        result = await service.get_settings_template_by_agent_type("non-existent", "test-token")

        assert result is None

    async def test_get_settings_template_by_agent_type_null_agent_type_raises(self, mock_http_client):
        """Test getting settings template with null agent type raises ValueError."""
        service = AgentSettingsService(http_client=mock_http_client)

        with pytest.raises(ValueError, match="Agent type cannot be null or empty"):
            await service.get_settings_template_by_agent_type("", "test-token")

    async def test_get_settings_template_by_agent_type_null_auth_token_raises(self, mock_http_client):
        """Test getting settings template with null auth token raises ValueError."""
        service = AgentSettingsService(http_client=mock_http_client)

        with pytest.raises(ValueError, match="Auth token cannot be null or empty"):
            await service.get_settings_template_by_agent_type("agent-type", "")

    async def test_set_settings_template_by_agent_type_success(self, mock_http_client):
        """Test setting settings template returns updated template on success."""
        template = AgentSettingsTemplate(
            id="template-123",
            agent_type="custom-agent",
            name="Test Template",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = template.model_dump_json(by_alias=True).encode()
        mock_response.raise_for_status = MagicMock()
        mock_http_client.put = AsyncMock(return_value=mock_response)

        service = AgentSettingsService(http_client=mock_http_client)
        result = await service.set_settings_template_by_agent_type(
            "custom-agent", template, "test-token"
        )

        assert result is not None
        assert result.id == "template-123"

    async def test_set_settings_template_by_agent_type_null_template_raises(self, mock_http_client):
        """Test setting settings template with null template raises ValueError."""
        service = AgentSettingsService(http_client=mock_http_client)

        with pytest.raises(ValueError, match="Template cannot be None"):
            await service.set_settings_template_by_agent_type("agent-type", None, "test-token")

    async def test_get_settings_by_agent_instance_success(self, mock_http_client):
        """Test getting settings returns settings on success."""
        expected_settings = AgentSettings(
            id="settings-123",
            agent_instance_id="instance-456",
            agent_type="custom-agent",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = expected_settings.model_dump_json(by_alias=True).encode()
        mock_response.raise_for_status = MagicMock()
        mock_http_client.get = AsyncMock(return_value=mock_response)

        service = AgentSettingsService(http_client=mock_http_client)
        result = await service.get_settings_by_agent_instance("instance-456", "test-token")

        assert result is not None
        assert result.id == "settings-123"
        assert result.agent_instance_id == "instance-456"

    async def test_get_settings_by_agent_instance_not_found(self, mock_http_client):
        """Test getting settings returns None on 404."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_http_client.get = AsyncMock(return_value=mock_response)

        service = AgentSettingsService(http_client=mock_http_client)
        result = await service.get_settings_by_agent_instance("non-existent", "test-token")

        assert result is None

    async def test_get_settings_by_agent_instance_null_instance_id_raises(self, mock_http_client):
        """Test getting settings with null instance ID raises ValueError."""
        service = AgentSettingsService(http_client=mock_http_client)

        with pytest.raises(ValueError, match="Agent instance ID cannot be null or empty"):
            await service.get_settings_by_agent_instance("", "test-token")

    async def test_set_settings_by_agent_instance_success(self, mock_http_client):
        """Test setting settings returns updated settings on success."""
        settings = AgentSettings(
            id="settings-123",
            agent_instance_id="instance-456",
            agent_type="custom-agent",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = settings.model_dump_json(by_alias=True).encode()
        mock_response.raise_for_status = MagicMock()
        mock_http_client.put = AsyncMock(return_value=mock_response)

        service = AgentSettingsService(http_client=mock_http_client)
        result = await service.set_settings_by_agent_instance(
            "instance-456", settings, "test-token"
        )

        assert result is not None
        assert result.id == "settings-123"

    async def test_set_settings_by_agent_instance_null_settings_raises(self, mock_http_client):
        """Test setting settings with null settings raises ValueError."""
        service = AgentSettingsService(http_client=mock_http_client)

        with pytest.raises(ValueError, match="Settings cannot be None"):
            await service.set_settings_by_agent_instance("instance-456", None, "test-token")

    async def test_context_manager(self, mock_http_client):
        """Test that service works as async context manager."""
        async with AgentSettingsService(http_client=mock_http_client) as service:
            assert service is not None

    async def test_close_closes_owned_client(self):
        """Test that close() closes the owned HTTP client."""
        service = AgentSettingsService()
        # Get client to initialize
        client = await service._get_client()
        assert client is not None

        await service.close()
        assert service._http_client is None


if __name__ == "__main__":
    unittest.main()
