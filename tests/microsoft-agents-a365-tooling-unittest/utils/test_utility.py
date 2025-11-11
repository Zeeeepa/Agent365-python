# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for utility functions in the tooling package.
"""

import os
from unittest.mock import patch

from microsoft_agents_a365.tooling.utils.utility import (
    get_tooling_gateway_for_digital_worker,
    get_mcp_base_url,
    build_mcp_server_url,
    _get_current_environment,
    _get_mcp_platform_base_url,
    get_ppapi_token_scope,
    MCP_PLATFORM_PROD_BASE_URL,
    PPAPI_TOKEN_SCOPE,
    PPAPI_TEST_TOKEN_SCOPE,
)


class TestUtilityFunctions:
    """Test class for utility functions."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Store original environment variables to restore after tests
        self.original_env = {
            key: os.environ.get(key)
            for key in [
                "ENVIRONMENT",
                "MCP_PLATFORM_ENDPOINT",
            ]
        }

    def teardown_method(self):
        """Clean up after each test method."""
        # Restore original environment variables
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_get_tooling_gateway_for_digital_worker(self):
        """Test get_tooling_gateway_for_digital_worker function."""
        # Arrange
        agent_user_id = "test-agent-123"

        # Act
        result = get_tooling_gateway_for_digital_worker(agent_user_id)

        # Assert
        expected = f"{MCP_PLATFORM_PROD_BASE_URL}/agentGateway/agentApplicationInstances/{agent_user_id}/mcpServers"
        assert result == expected

    @patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": "https://custom.endpoint.com"}, clear=False)
    def test_get_tooling_gateway_with_custom_endpoint(self):
        """Test get_tooling_gateway_for_digital_worker with custom MCP platform endpoint."""
        # Arrange
        agent_user_id = "test-agent-456"

        # Act
        result = get_tooling_gateway_for_digital_worker(agent_user_id)

        # Assert
        expected = "https://custom.endpoint.com/agentGateway/agentApplicationInstances/test-agent-456/mcpServers"
        assert result == expected

    def test_get_mcp_base_url_production(self):
        """Test get_mcp_base_url in production environment."""
        # Arrange - Set production environment
        os.environ.pop("ENVIRONMENT", None)

        # Act
        result = get_mcp_base_url()

        # Assert
        expected = f"{MCP_PLATFORM_PROD_BASE_URL}/mcp/environments"
        assert result == expected

    @patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": "https://custom.endpoint.com"}, clear=False)
    def test_get_mcp_base_url_with_custom_endpoint(self):
        """Test get_mcp_base_url with custom MCP platform endpoint."""
        # Act
        result = get_mcp_base_url()

        # Assert
        expected = "https://custom.endpoint.com/mcp/environments"
        assert result == expected

    def test_build_mcp_server_url_production(self):
        """Test build_mcp_server_url in production environment."""
        # Arrange
        environment_id = "prod-env-123"
        server_name = "mail_server"

        # Act
        result = build_mcp_server_url(environment_id, server_name)

        # Assert
        expected = (
            f"{MCP_PLATFORM_PROD_BASE_URL}/mcp/environments/{environment_id}/servers/{server_name}"
        )
        assert result == expected

    @patch.dict(os.environ, {"ENVIRONMENT": "Development"}, clear=False)
    def test_build_mcp_server_url_development_platform_mode(self):
        """Test build_mcp_server_url in development with platform mode."""
        # Arrange
        environment_id = "dev-env-456"
        server_name = "platform_server"

        # Act
        result = build_mcp_server_url(environment_id, server_name)

        # Assert
        expected = (
            f"{MCP_PLATFORM_PROD_BASE_URL}/mcp/environments/{environment_id}/servers/{server_name}"
        )
        assert result == expected

    def test_get_current_environment_default(self):
        """Test _get_current_environment returns default when no env vars set."""
        # Arrange - Clear environment variables
        os.environ.pop("ENVIRONMENT", None)

        # Act
        result = _get_current_environment()

        # Assert
        assert result == "Development"

    @patch.dict(os.environ, {"ENVIRONMENT": "Production"}, clear=False)
    def test_get_current_environment_set(self):
        """Test _get_current_environment returns ENVIRONMENT value."""
        # Act
        result = _get_current_environment()

        # Assert
        assert result == "Production"

    def test_get_mcp_platform_base_url_default(self):
        """Test _get_mcp_platform_base_url returns default production URL."""
        # Arrange
        os.environ.pop("MCP_PLATFORM_ENDPOINT", None)

        # Act
        result = _get_mcp_platform_base_url()

        # Assert
        assert result == MCP_PLATFORM_PROD_BASE_URL

    @patch.dict(os.environ, {"MCP_PLATFORM_ENDPOINT": "https://test.platform.com"}, clear=False)
    def test_get_mcp_platform_base_url_custom(self):
        """Test _get_mcp_platform_base_url returns custom endpoint."""
        # Act
        result = _get_mcp_platform_base_url()

        # Assert
        assert result == "https://test.platform.com"

    def test_get_ppapi_token_scope_production(self):
        """Test get_ppapi_token_scope returns production scope."""
        # Arrange - Set environment to production explicitly
        os.environ.pop("ENVIRONMENT", None)
        # The _get_current_environment defaults to "Development", so we need to set it to something else
        os.environ["ENVIRONMENT"] = "Production"

        # Act
        result = get_ppapi_token_scope()

        # Assert
        expected = [PPAPI_TOKEN_SCOPE + "/.default"]
        assert result == expected

    @patch.dict(os.environ, {"ENVIRONMENT": "Development"}, clear=False)
    def test_get_ppapi_token_scope_development(self):
        """Test get_ppapi_token_scope returns test scope in development."""
        # Act
        result = get_ppapi_token_scope()

        # Assert
        expected = [PPAPI_TEST_TOKEN_SCOPE + "/.default"]
        assert result == expected

    def test_constants_values(self):
        """Test that constants have expected values."""
        # Assert
        assert MCP_PLATFORM_PROD_BASE_URL == "https://agent365.svc.cloud.microsoft"
        assert PPAPI_TOKEN_SCOPE == "https://api.powerplatform.com"
        assert PPAPI_TEST_TOKEN_SCOPE == "https://api.test.powerplatform.com"

    def test_get_tooling_gateway_empty_agent_id(self):
        """Test get_tooling_gateway_for_digital_worker with empty agent ID."""
        # Arrange
        agent_user_id = ""

        # Act
        result = get_tooling_gateway_for_digital_worker(agent_user_id)

        # Assert - Function should still work but produce invalid URL
        expected = (
            f"{MCP_PLATFORM_PROD_BASE_URL}/agentGateway/agentApplicationInstances//mcpServers"
        )
        assert result == expected

    def test_build_mcp_server_url_empty_params(self):
        """Test build_mcp_server_url with empty parameters."""
        # Arrange
        environment_id = ""
        server_name = ""

        # Act
        result = build_mcp_server_url(environment_id, server_name)

        # Assert
        expected = f"{MCP_PLATFORM_PROD_BASE_URL}/mcp/environments//servers/"
        assert result == expected
