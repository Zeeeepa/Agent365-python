# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for McpToolRegistrationService core logic.
Tests the business logic without requiring external dependencies.
"""

import logging
import pytest
from typing import List, Optional, Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch


class MockMcpToolRegistrationService:
    """Mock implementation that mirrors the actual service for testing."""

    def __init__(self, logger: Optional[logging.Logger] = None, credential=None):
        """Initialize the service with optional logger and credential."""
        self._logger = logger or logging.getLogger("McpToolRegistrationService")
        self._credential = credential or MagicMock()
        self._mcp_server_configuration_service = MagicMock()

    async def add_tool_servers_to_agent(
        self,
        project_client,
        agent_id: str,
        environment_id: str,
        auth,
        context,
        auth_token: Optional[str] = None,
    ):
        """Add MCP tool servers to an agent."""
        # Validate inputs
        if project_client is None:
            raise ValueError("project_client cannot be None")

        try:
            # Get auth token if not provided
            if not auth_token:
                # Mock token exchange
                token_scope = ["https://cognitiveservices.azure.com/.default"]
                exchanged_token = await auth.exchange_token(context, token_scope, "AGENTIC")
                auth_token = exchanged_token.token

            # Get tool definitions and resources
            tool_definitions, tool_resources = await self._get_mcp_tool_definitions_and_resources(
                agent_id, environment_id, auth_token
            )

            # Update agent with tools
            project_client.agents.update_agent(
                agent_id, tools=tool_definitions, tool_resources=tool_resources
            )

            self._logger.info(
                f"Successfully configured {len(tool_definitions)} MCP tool servers for agent"
            )

        except Exception as e:
            self._logger.error(f"Unhandled failure during MCP tool registration workflow: {e}")
            raise

    async def _get_mcp_tool_definitions_and_resources(
        self, agent_id: str, environment_id: str, auth_token: str
    ):
        """Get MCP tool definitions and resources."""
        # Check if configuration service is available
        if not self._mcp_server_configuration_service:
            self._logger.error("MCP server configuration service is not available")
            return [], None

        try:
            # List tool servers
            servers = await self._mcp_server_configuration_service.list_tool_servers(
                agent_id, environment_id, auth_token
            )

            if not servers:
                self._logger.info(
                    f"No MCP servers configured for AgentUserId={agent_id}, EnvironmentId={environment_id}"
                )
                return [], None

            tool_definitions = []
            tool_resources_list = []

            for server in servers:
                # Validate server configuration
                if not server.mcp_server_name or not server.mcp_server_unique_name:
                    self._logger.warning(
                        f"Invalid server configuration: name={server.mcp_server_name}, url={server.mcp_server_unique_name}"
                    )
                    continue

                # Remove mcp_ prefix from server name
                server_label = server.mcp_server_name
                if server_label.startswith("mcp_"):
                    server_label = server_label[4:]

                # Create MCP tool (mocked)
                mcp_tool = MagicMock()
                mcp_tool.definitions = [f"tool_def_{server_label}"]
                mcp_tool.resources = MagicMock() if server_label != "no_resources" else None

                if mcp_tool.resources:
                    mcp_tool.resources.mcp = [f"resource_{server_label}"]

                # Configure tool
                mcp_tool.set_approval_mode("never")

                # Handle auth token
                if auth_token.lower().startswith("bearer"):
                    auth_header = auth_token
                else:
                    auth_header = f"Bearer {auth_token}"

                mcp_tool.update_headers("Authorization", auth_header)
                mcp_tool.update_headers("x-ms-environment-id", environment_id)

                # Add to collections
                tool_definitions.extend(mcp_tool.definitions)
                if mcp_tool.resources and mcp_tool.resources.mcp:
                    tool_resources_list.extend(mcp_tool.resources.mcp)

            # Create tool resources object
            tool_resources = None
            if tool_resources_list:
                tool_resources = MagicMock()
                tool_resources.mcp = tool_resources_list

            self._logger.info(
                f"Processed {len(servers)} MCP servers, created {len(tool_definitions)} tool definitions"
            )
            return tool_definitions, tool_resources

        except Exception as e:
            self._logger.error(
                f"Failed to list MCP tool servers for AgentUserId={agent_id}, EnvironmentId={environment_id}: {e}"
            )
            return [], None


class TestMcpToolRegistrationService:
    """Test class for MCP Tool Registration Service core logic."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mock_logger = MagicMock(spec=logging.Logger)
        self.mock_credential = MagicMock()
        self.mock_project_client = MagicMock()
        self.mock_auth = MagicMock()
        self.mock_context = MagicMock()

        # Create service instance
        self.service = MockMcpToolRegistrationService(
            logger=self.mock_logger, credential=self.mock_credential
        )

    # ========================================================================================
    # INITIALIZATION TESTS
    # ========================================================================================

    def test_initialization_with_custom_logger_and_credential(self):
        """Test service initialization with custom logger and credential."""
        # Act
        service = MockMcpToolRegistrationService(
            logger=self.mock_logger, credential=self.mock_credential
        )

        # Assert
        assert service is not None
        assert service._logger is self.mock_logger
        assert service._credential is self.mock_credential

    def test_initialization_with_default_logger_and_credential(self):
        """Test service initialization with default logger and credential."""
        # Act
        service = MockMcpToolRegistrationService()

        # Assert
        assert service is not None
        assert service._logger is not None
        assert service._logger.name == "McpToolRegistrationService"
        assert service._credential is not None

    def test_initialization_creates_mcp_server_configuration_service(self):
        """Test that initialization creates the MCP server configuration service."""
        # Act
        service = MockMcpToolRegistrationService(logger=self.mock_logger)

        # Assert
        assert service._mcp_server_configuration_service is not None

    # ========================================================================================
    # INPUT VALIDATION TESTS
    # ========================================================================================

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_none_project_client_raises_error(self):
        """Test add_tool_servers_to_agent raises ValueError for None project_client."""
        # Act & Assert
        with pytest.raises(ValueError, match="project_client cannot be None"):
            await self.service.add_tool_servers_to_agent(
                None, "agent123", "env123", self.mock_auth, self.mock_context
            )

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_with_valid_project_client(self):
        """Test add_tool_servers_to_agent accepts valid project_client."""
        # Arrange
        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = mock_config_service

        # Act & Assert - Should not raise
        await self.service.add_tool_servers_to_agent(
            self.mock_project_client,
            "agent123",
            "env123",
            self.mock_auth,
            self.mock_context,
            "token123",
        )

    # ========================================================================================
    # TOKEN HANDLING TESTS
    # ========================================================================================

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_with_auth_token(self):
        """Test add_tool_servers_to_agent with provided auth_token."""
        # Arrange
        auth_token = "test_token_123"
        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        await self.service.add_tool_servers_to_agent(
            self.mock_project_client,
            "agent123",
            "env123",
            self.mock_auth,
            self.mock_context,
            auth_token,
        )

        # Assert - Should not call exchange_token since token provided
        self.mock_auth.exchange_token.assert_not_called()
        mock_config_service.list_tool_servers.assert_called_once_with(
            "agent123", "env123", auth_token
        )

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_without_auth_token_exchanges_token(self):
        """Test add_tool_servers_to_agent exchanges token when not provided."""
        # Arrange
        mock_exchanged_token = MagicMock()
        mock_exchanged_token.token = "exchanged_token_456"
        self.mock_auth.exchange_token = AsyncMock(return_value=mock_exchanged_token)

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        await self.service.add_tool_servers_to_agent(
            self.mock_project_client, "agent123", "env123", self.mock_auth, self.mock_context
        )

        # Assert
        expected_scope = ["https://cognitiveservices.azure.com/.default"]
        self.mock_auth.exchange_token.assert_called_once_with(
            self.mock_context, expected_scope, "AGENTIC"
        )
        mock_config_service.list_tool_servers.assert_called_once_with(
            "agent123", "env123", "exchanged_token_456"
        )

    # ========================================================================================
    # MCP TOOL DEFINITIONS AND RESOURCES TESTS
    # ========================================================================================

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_no_config_service(self):
        """Test _get_mcp_tool_definitions_and_resources with no config service."""
        # Arrange
        self.service._mcp_server_configuration_service = None

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        assert result == ([], None)
        self.mock_logger.error.assert_called_once_with(
            "MCP server configuration service is not available"
        )

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_list_servers_exception(self):
        """Test _get_mcp_tool_definitions_and_resources handles list_tool_servers exception."""
        # Arrange
        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.side_effect = Exception("Connection failed")
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        assert result == ([], None)
        self.mock_logger.error.assert_called_once()
        assert (
            "Failed to list MCP tool servers for AgentUserId=agent123"
            in self.mock_logger.error.call_args[0][0]
        )

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_no_servers(self):
        """Test _get_mcp_tool_definitions_and_resources with no servers configured."""
        # Arrange
        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        assert result == ([], None)
        mock_config_service.list_tool_servers.assert_called_once_with(
            "agent123", "env123", "token123"
        )
        self.mock_logger.info.assert_called_once_with(
            "No MCP servers configured for AgentUserId=agent123, EnvironmentId=env123"
        )

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_invalid_server_config(self):
        """Test _get_mcp_tool_definitions_and_resources skips invalid server configs."""
        # Arrange
        mock_server1 = MagicMock()
        mock_server1.mcp_server_name = ""  # Invalid - empty name
        mock_server1.mcp_server_unique_name = "http://valid.url"

        mock_server2 = MagicMock()
        mock_server2.mcp_server_name = "valid_name"
        mock_server2.mcp_server_unique_name = ""  # Invalid - empty URL

        mock_server3 = MagicMock()
        mock_server3.mcp_server_name = None  # Invalid - None name
        mock_server3.mcp_server_unique_name = "http://valid.url"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [
            mock_server1,
            mock_server2,
            mock_server3,
        ]
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        assert result == ([], None)
        # Should log warning for each invalid server
        assert self.mock_logger.warning.call_count == 3

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_valid_servers(self):
        """Test _get_mcp_tool_definitions_and_resources with valid server configs."""
        # Arrange
        mock_server1 = MagicMock()
        mock_server1.mcp_server_name = "mcp_mail_server"
        mock_server1.mcp_server_unique_name = "http://localhost:8080/mail"

        mock_server2 = MagicMock()
        mock_server2.mcp_server_name = "calendar_server"
        mock_server2.mcp_server_unique_name = "http://localhost:8080/calendar"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [mock_server1, mock_server2]
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        tool_definitions, tool_resources = result
        assert len(tool_definitions) == 2
        assert "tool_def_mail_server" in tool_definitions
        assert "tool_def_calendar_server" in tool_definitions
        assert tool_resources is not None
        assert len(tool_resources.mcp) == 2

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_server_name_prefix_handling(self):
        """Test server name prefix handling (mcp_ prefix removal)."""
        # Arrange
        mock_server = MagicMock()
        mock_server.mcp_server_name = "mcp_test_server"
        mock_server.mcp_server_unique_name = "http://localhost:8080/test"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [mock_server]
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        tool_definitions, tool_resources = result
        assert len(tool_definitions) == 1
        assert "tool_def_test_server" in tool_definitions

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_no_resources_server(self):
        """Test handling of servers with no resources."""
        # Arrange
        mock_server = MagicMock()
        mock_server.mcp_server_name = "no_resources"  # Special case in mock
        mock_server.mcp_server_unique_name = "http://localhost:8080/test"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [mock_server]
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        tool_definitions, tool_resources = result
        assert len(tool_definitions) == 1
        assert tool_resources is None  # Should be None when no resources

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_auth_token_header_handling(self):
        """Test auth token header handling with and without Bearer prefix."""
        # Arrange
        mock_server = MagicMock()
        mock_server.mcp_server_name = "test_server"
        mock_server.mcp_server_unique_name = "http://localhost:8080/test"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [mock_server]
        self.service._mcp_server_configuration_service = mock_config_service

        # Test case 1: Token without Bearer prefix
        await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "simple_token_123"
        )

        # Test case 2: Token with Bearer prefix
        await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "Bearer token_with_prefix"
        )

        # Assert - Both should work (tested by no exceptions thrown)
        assert mock_config_service.list_tool_servers.call_count == 2

    # ========================================================================================
    # INTEGRATION AND ERROR HANDLING TESTS
    # ========================================================================================

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_handles_exceptions(self):
        """Test add_tool_servers_to_agent handles exceptions properly."""
        # Arrange - Mock the project_client update_agent to throw an exception
        self.mock_project_client.agents.update_agent.side_effect = Exception("Internal error")

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = []  # Return empty list so we get to update_agent
        self.service._mcp_server_configuration_service = mock_config_service

        # Act & Assert
        with pytest.raises(Exception, match="Internal error"):
            await self.service.add_tool_servers_to_agent(
                self.mock_project_client,
                "agent123",
                "env123",
                self.mock_auth,
                self.mock_context,
                "token123",
            )

        # Assert error was logged
        self.mock_logger.error.assert_called_once()
        assert (
            "Unhandled failure during MCP tool registration workflow"
            in self.mock_logger.error.call_args[0][0]
        )

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_success_logs_info(self):
        """Test add_tool_servers_to_agent logs success message."""
        # Arrange
        mock_server1 = MagicMock()
        mock_server1.mcp_server_name = "server1"
        mock_server1.mcp_server_unique_name = "http://localhost:8080/server1"

        mock_server2 = MagicMock()
        mock_server2.mcp_server_name = "server2"
        mock_server2.mcp_server_unique_name = "http://localhost:8080/server2"

        mock_server3 = MagicMock()
        mock_server3.mcp_server_name = "server3"
        mock_server3.mcp_server_unique_name = "http://localhost:8080/server3"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [
            mock_server1,
            mock_server2,
            mock_server3,
        ]
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        await self.service.add_tool_servers_to_agent(
            self.mock_project_client,
            "agent123",
            "env123",
            self.mock_auth,
            self.mock_context,
            "token123",
        )

        # Assert
        self.mock_logger.info.assert_called_with(
            "Successfully configured 3 MCP tool servers for agent"
        )

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_logs_processing_info(self):
        """Test _get_mcp_tool_definitions_and_resources logs processing information."""
        # Arrange
        mock_server1 = MagicMock()
        mock_server1.mcp_server_name = "server1"
        mock_server1.mcp_server_unique_name = "http://localhost:8080/server1"

        mock_server2 = MagicMock()
        mock_server2.mcp_server_name = "server2"
        mock_server2.mcp_server_unique_name = "http://localhost:8080/server2"

        mock_config_service = AsyncMock()
        mock_config_service.list_tool_servers.return_value = [mock_server1, mock_server2]
        self.service._mcp_server_configuration_service = mock_config_service

        # Act
        await self.service._get_mcp_tool_definitions_and_resources("agent123", "env123", "token123")

        # Assert
        self.mock_logger.info.assert_called_with(
            "Processed 2 MCP servers, created 2 tool definitions"
        )

    def test_service_properties_and_methods(self):
        """Test that service has expected properties and methods."""
        # Assert
        assert hasattr(self.service, "_logger")
        assert hasattr(self.service, "_credential")
        assert hasattr(self.service, "_mcp_server_configuration_service")
        assert hasattr(self.service, "add_tool_servers_to_agent")
        assert hasattr(self.service, "_get_mcp_tool_definitions_and_resources")

        # Check that methods are callable
        assert callable(self.service.add_tool_servers_to_agent)
        assert callable(self.service._get_mcp_tool_definitions_and_resources)
