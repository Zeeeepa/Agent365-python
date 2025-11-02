# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Unit tests for utility functions in the tooling package.
"""

import os
import pytest
from unittest.mock import patch

# Add the parent directory to the path to import the modules
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent.parent / "libraries" / "microsoft-agents-a365-tooling"),
)

from microsoft_agents_a365.tooling.utils.utility import (
    get_tooling_gateway_for_digital_worker,
    get_mcp_base_url,
    build_mcp_server_url,
    _get_current_environment,
    _get_mcp_platform_base_url,
    get_tools_mode,
    get_ppapi_token_scope,
    ToolsMode,
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
                "ASPNETCORE_ENVIRONMENT",
                "DOTNET_ENVIRONMENT",
                "MCP_PLATFORM_ENDPOINT",
                "TOOLS_MODE",
                "MOCK_MCP_SERVER_URL",
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
        os.environ.pop("ASPNETCORE_ENVIRONMENT", None)
        os.environ.pop("DOTNET_ENVIRONMENT", None)

        # Act
        result = get_mcp_base_url()

        # Assert
        expected = f"{MCP_PLATFORM_PROD_BASE_URL}/mcp/environments"
        assert result == expected

    @patch.dict(os.environ, {"ASPNETCORE_ENVIRONMENT": "Development"}, clear=False)
    def test_get_mcp_base_url_development_default_mode(self):
        """Test get_mcp_base_url in development environment with default mode."""
        # Act
        result = get_mcp_base_url()

        # Assert
        expected = f"{MCP_PLATFORM_PROD_BASE_URL}/mcp/environments"
        assert result == expected

    @patch.dict(
        os.environ,
        {"ASPNETCORE_ENVIRONMENT": "Development", "TOOLS_MODE": "MockMCPServer"},
        clear=False,
    )
    def test_get_mcp_base_url_development_mock_mode_default_url(self):
        """Test get_mcp_base_url in development with mock mode using default URL."""
        # Act
        result = get_mcp_base_url()

        # Assert
        expected = "http://localhost:5309/mcp-mock/agents/servers"
        assert result == expected

    @patch.dict(
        os.environ,
        {
            "ASPNETCORE_ENVIRONMENT": "Development",
            "TOOLS_MODE": "MockMCPServer",
            "MOCK_MCP_SERVER_URL": "http://custom-mock:8080/mock/servers",
        },
        clear=False,
    )
    def test_get_mcp_base_url_development_mock_mode_custom_url(self):
        """Test get_mcp_base_url in development with mock mode using custom URL."""
        # Act
        result = get_mcp_base_url()

        # Assert
        expected = "http://custom-mock:8080/mock/servers"
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

    @patch.dict(
        os.environ,
        {"ASPNETCORE_ENVIRONMENT": "Development", "TOOLS_MODE": "MockMCPServer"},
        clear=False,
    )
    def test_build_mcp_server_url_development_mock_mode(self):
        """Test build_mcp_server_url in development with mock mode."""
        # Arrange
        environment_id = "dev-env-123"
        server_name = "test_server"

        # Act
        result = build_mcp_server_url(environment_id, server_name)

        # Assert
        expected = "http://localhost:5309/mcp-mock/agents/servers/test_server"
        assert result == expected

    @patch.dict(os.environ, {"ASPNETCORE_ENVIRONMENT": "Development"}, clear=False)
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
        os.environ.pop("ASPNETCORE_ENVIRONMENT", None)
        os.environ.pop("DOTNET_ENVIRONMENT", None)

        # Act
        result = _get_current_environment()

        # Assert
        assert result == "Development"

    @patch.dict(os.environ, {"ASPNETCORE_ENVIRONMENT": "Production"}, clear=False)
    def test_get_current_environment_aspnetcore(self):
        """Test _get_current_environment returns ASPNETCORE_ENVIRONMENT value."""
        # Act
        result = _get_current_environment()

        # Assert
        assert result == "Production"

    @patch.dict(os.environ, {"DOTNET_ENVIRONMENT": "Staging"}, clear=False)
    def test_get_current_environment_dotnet(self):
        """Test _get_current_environment returns DOTNET_ENVIRONMENT value."""
        # Act
        result = _get_current_environment()

        # Assert
        assert result == "Staging"

    @patch.dict(
        os.environ,
        {"ASPNETCORE_ENVIRONMENT": "Production", "DOTNET_ENVIRONMENT": "Staging"},
        clear=False,
    )
    def test_get_current_environment_aspnetcore_priority(self):
        """Test _get_current_environment prioritizes ASPNETCORE_ENVIRONMENT."""
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

    def test_get_tools_mode_default(self):
        """Test get_tools_mode returns default MCP_PLATFORM mode."""
        # Arrange
        os.environ.pop("TOOLS_MODE", None)

        # Act
        result = get_tools_mode()

        # Assert
        assert result == ToolsMode.MCP_PLATFORM

    @patch.dict(os.environ, {"TOOLS_MODE": "MockMCPServer"}, clear=False)
    def test_get_tools_mode_mock(self):
        """Test get_tools_mode returns MOCK_MCP_SERVER mode."""
        # Act
        result = get_tools_mode()

        # Assert
        assert result == ToolsMode.MOCK_MCP_SERVER

    @patch.dict(os.environ, {"TOOLS_MODE": "mockmcpserver"}, clear=False)
    def test_get_tools_mode_mock_lowercase(self):
        """Test get_tools_mode handles lowercase input."""
        # Act
        result = get_tools_mode()

        # Assert
        assert result == ToolsMode.MOCK_MCP_SERVER

    @patch.dict(os.environ, {"TOOLS_MODE": "MCPPlatform"}, clear=False)
    def test_get_tools_mode_platform_explicit(self):
        """Test get_tools_mode returns MCP_PLATFORM when explicitly set."""
        # Act
        result = get_tools_mode()

        # Assert
        assert result == ToolsMode.MCP_PLATFORM

    @patch.dict(os.environ, {"TOOLS_MODE": "InvalidMode"}, clear=False)
    def test_get_tools_mode_invalid_defaults_to_platform(self):
        """Test get_tools_mode defaults to MCP_PLATFORM for invalid values."""
        # Act
        result = get_tools_mode()

        # Assert
        assert result == ToolsMode.MCP_PLATFORM

    def test_get_ppapi_token_scope_production(self):
        """Test get_ppapi_token_scope returns production scope."""
        # Arrange - Set environment to production explicitly
        os.environ.pop("ASPNETCORE_ENVIRONMENT", None)
        os.environ.pop("DOTNET_ENVIRONMENT", None)
        # The _get_current_environment defaults to "Development", so we need to set it to something else
        os.environ["ASPNETCORE_ENVIRONMENT"] = "Production"

        # Act
        result = get_ppapi_token_scope()

        # Assert
        expected = [PPAPI_TOKEN_SCOPE + "/.default"]
        assert result == expected

    @patch.dict(os.environ, {"ASPNETCORE_ENVIRONMENT": "Development"}, clear=False)
    def test_get_ppapi_token_scope_development(self):
        """Test get_ppapi_token_scope returns test scope in development."""
        # Act
        result = get_ppapi_token_scope()

        # Assert
        expected = [PPAPI_TEST_TOKEN_SCOPE + "/.default"]
        assert result == expected

    @patch.dict(os.environ, {"DOTNET_ENVIRONMENT": "Development"}, clear=False)
    def test_get_ppapi_token_scope_development_dotnet_env(self):
        """Test get_ppapi_token_scope works with DOTNET_ENVIRONMENT."""
        # Act
        result = get_ppapi_token_scope()

        # Assert
        expected = [PPAPI_TEST_TOKEN_SCOPE + "/.default"]
        assert result == expected

    def test_tools_mode_enum_values(self):
        """Test ToolsMode enum has expected values."""
        # Assert
        assert ToolsMode.MOCK_MCP_SERVER.value == "MockMCPServer"
        assert ToolsMode.MCP_PLATFORM.value == "MCPPlatform"

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
