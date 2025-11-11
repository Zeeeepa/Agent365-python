# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for McpToolRegistrationService business logic.
This tests the service implementation flow with mock dependencies.
"""

import logging
import pytest
from dataclasses import dataclass
from typing import List, Optional
from unittest.mock import AsyncMock, MagicMock


@dataclass
class MockMCPServerConfig:
    """Mock configuration for MCP server."""

    mcp_server_name: str
    mcp_server_unique_name: str


@dataclass
class MockMcpTool:
    """Mock MCP tool with definitions and resources."""

    definitions: List[str]
    resources: Optional[object] = None

    def update_headers(self, header_name: str, header_value: str):
        """Mock method to update headers."""
        pass


@dataclass
class MockToolResources:
    """Mock tool resources."""

    mcp: List[str]


class MockMcpToolRegistrationService:
    """
    Mock implementation of McpToolRegistrationService that replicates the real service logic.
    This is used to test the business logic without requiring full environment setup.
    """

    def __init__(self, logger: Optional[logging.Logger] = None, credential=None):
        """Initialize the service with optional logger and credential."""
        self._logger = logger or logging.getLogger("McpToolRegistrationService")
        self._credential = credential or MagicMock()
        self._mcp_server_configuration_service = None

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
                # Get Power Platform API token scope
                token_scope = ["https://api.powerplatform.com/.default"]
                exchanged_token = await auth.exchange_token(context, token_scope, "AGENTIC")
                auth_token = exchanged_token.token

            # Get tool definitions and resources
            tool_definitions, tool_resources = await self._get_mcp_tool_definitions_and_resources(
                agent_id, environment_id, auth_token
            )

            # Update agent with tools if we have definitions
            if tool_definitions:
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
        """Get MCP tool definitions and resources from configured servers."""
        # Check if configuration service is available
        if not self._mcp_server_configuration_service:
            self._logger.error("MCP server configuration service is not available")
            return [], None

        try:
            # List tool servers from configuration service
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

                # Remove mcp_ prefix from server name if present
                server_label = server.mcp_server_name
                if server_label.startswith("mcp_"):
                    server_label = server_label[4:]

                # Create MCP tool with server configuration
                mcp_tool = MockMcpTool(
                    definitions=[f"definition_{server_label}"],
                    resources=MockToolResources(mcp=[f"resource_{server_label}"]),
                )

                # Handle auth token - add Bearer prefix if not present
                if auth_token.lower().startswith("bearer"):
                    auth_header = auth_token
                else:
                    auth_header = f"Bearer {auth_token}"

                # Update tool headers with authentication and environment
                mcp_tool.update_headers("Authorization", auth_header)
                mcp_tool.update_headers("x-ms-environment-id", environment_id)

                # Collect definitions and resources
                tool_definitions.extend(mcp_tool.definitions)
                if mcp_tool.resources and mcp_tool.resources.mcp:
                    tool_resources_list.extend(mcp_tool.resources.mcp)

            # Create tool resources object if we have any resources
            tool_resources = None
            if tool_resources_list:
                tool_resources = MockToolResources(mcp=tool_resources_list)

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
    """Test class for MCP Tool Registration Service business logic."""

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

    # ========================================================================================
    # TOKEN HANDLING TESTS
    # ========================================================================================

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_with_auth_token(self):
        """Test add_tool_servers_to_agent with provided auth_token."""
        # Arrange
        auth_token = "test_token_123"
        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = config_service

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
        config_service.list_tool_servers.assert_called_once_with("agent123", "env123", auth_token)

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_without_auth_token_exchanges_token(self):
        """Test add_tool_servers_to_agent exchanges token when not provided."""
        # Arrange
        exchanged_token = MagicMock()
        exchanged_token.token = "exchanged_token_456"
        self.mock_auth.exchange_token = AsyncMock(return_value=exchanged_token)

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = config_service

        # Act
        await self.service.add_tool_servers_to_agent(
            self.mock_project_client, "agent123", "env123", self.mock_auth, self.mock_context
        )

        # Assert - Verify token was exchanged with Power Platform API scope
        expected_scope = ["https://api.powerplatform.com/.default"]
        self.mock_auth.exchange_token.assert_called_once_with(
            self.mock_context, expected_scope, "AGENTIC"
        )
        config_service.list_tool_servers.assert_called_once_with(
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
        config_service = AsyncMock()
        config_service.list_tool_servers.side_effect = Exception("Connection failed")
        self.service._mcp_server_configuration_service = config_service

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
        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = []
        self.service._mcp_server_configuration_service = config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        assert result == ([], None)
        config_service.list_tool_servers.assert_called_once_with("agent123", "env123", "token123")
        self.mock_logger.info.assert_called_once_with(
            "No MCP servers configured for AgentUserId=agent123, EnvironmentId=env123"
        )

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_invalid_server_config(self):
        """Test _get_mcp_tool_definitions_and_resources skips invalid server configs."""
        # Arrange
        server1 = MockMCPServerConfig(
            mcp_server_name="",  # Invalid - empty name
            mcp_server_unique_name="http://valid.url",
        )
        server2 = MockMCPServerConfig(
            mcp_server_name="valid_name",
            mcp_server_unique_name="",  # Invalid - empty URL
        )
        server3 = MockMCPServerConfig(
            mcp_server_name=None,  # Invalid - None name
            mcp_server_unique_name="http://valid.url",
        )

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = [
            server1,
            server2,
            server3,
        ]
        self.service._mcp_server_configuration_service = config_service

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
        server1 = MockMCPServerConfig(
            mcp_server_name="mcp_mail_server", mcp_server_unique_name="http://localhost:8080/mail"
        )
        server2 = MockMCPServerConfig(
            mcp_server_name="calendar_server",
            mcp_server_unique_name="http://localhost:8080/calendar",
        )

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = [server1, server2]
        self.service._mcp_server_configuration_service = config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        tool_definitions, tool_resources = result
        assert len(tool_definitions) == 2
        assert "definition_mail_server" in tool_definitions
        assert "definition_calendar_server" in tool_definitions
        assert tool_resources is not None
        assert len(tool_resources.mcp) == 2
        assert "resource_mail_server" in tool_resources.mcp
        assert "resource_calendar_server" in tool_resources.mcp

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_server_name_prefix_handling(self):
        """Test server name prefix handling (mcp_ prefix removal)."""
        # Arrange
        server = MockMCPServerConfig(
            mcp_server_name="mcp_test_server", mcp_server_unique_name="http://localhost:8080/test"
        )

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = [server]
        self.service._mcp_server_configuration_service = config_service

        # Act
        result = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "token123"
        )

        # Assert
        tool_definitions, tool_resources = result
        assert len(tool_definitions) == 1
        # Verify the mcp_ prefix was removed
        assert "definition_test_server" in tool_definitions
        assert "resource_test_server" in tool_resources.mcp

    @pytest.mark.asyncio
    async def test_get_mcp_tool_definitions_and_resources_auth_token_bearer_prefix(self):
        """Test auth token header handling with and without Bearer prefix."""
        # Arrange
        server = MockMCPServerConfig(
            mcp_server_name="test_server", mcp_server_unique_name="http://localhost:8080/test"
        )

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = [server]
        self.service._mcp_server_configuration_service = config_service

        # Test case 1: Token without Bearer prefix
        result1 = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "simple_token_123"
        )

        # Test case 2: Token with Bearer prefix
        result2 = await self.service._get_mcp_tool_definitions_and_resources(
            "agent123", "env123", "Bearer token_with_prefix"
        )

        # Assert - Both should work (tested by successful execution)
        assert len(result1[0]) == 1
        assert len(result2[0]) == 1
        assert config_service.list_tool_servers.call_count == 2

    # ========================================================================================
    # INTEGRATION AND ERROR HANDLING TESTS
    # ========================================================================================

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_handles_exceptions(self):
        """Test add_tool_servers_to_agent handles exceptions properly."""
        # Arrange - Mock the project_client update_agent to throw an exception
        self.mock_project_client.agents.update_agent.side_effect = Exception("Internal error")

        config_service = AsyncMock()
        server = MockMCPServerConfig(
            mcp_server_name="test_server", mcp_server_unique_name="http://localhost:8080/test"
        )
        config_service.list_tool_servers.return_value = [
            server
        ]  # Return server so update_agent is called
        self.service._mcp_server_configuration_service = config_service

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
        server1 = MockMCPServerConfig(
            mcp_server_name="server1", mcp_server_unique_name="http://localhost:8080/server1"
        )
        server2 = MockMCPServerConfig(
            mcp_server_name="server2", mcp_server_unique_name="http://localhost:8080/server2"
        )
        server3 = MockMCPServerConfig(
            mcp_server_name="server3", mcp_server_unique_name="http://localhost:8080/server3"
        )

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = [
            server1,
            server2,
            server3,
        ]
        self.service._mcp_server_configuration_service = config_service

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
        server1 = MockMCPServerConfig(
            mcp_server_name="server1", mcp_server_unique_name="http://localhost:8080/server1"
        )
        server2 = MockMCPServerConfig(
            mcp_server_name="server2", mcp_server_unique_name="http://localhost:8080/server2"
        )

        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = [server1, server2]
        self.service._mcp_server_configuration_service = config_service

        # Act
        await self.service._get_mcp_tool_definitions_and_resources("agent123", "env123", "token123")

        # Assert
        self.mock_logger.info.assert_called_with(
            "Processed 2 MCP servers, created 2 tool definitions"
        )

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_no_definitions_skips_update(self):
        """Test that agent is not updated when no tool definitions are found."""
        # Arrange
        config_service = AsyncMock()
        config_service.list_tool_servers.return_value = []  # No servers
        self.service._mcp_server_configuration_service = config_service

        # Act
        await self.service.add_tool_servers_to_agent(
            self.mock_project_client,
            "agent123",
            "env123",
            self.mock_auth,
            self.mock_context,
            "token123",
        )

        # Assert - update_agent should not be called when there are no tool definitions
        self.mock_project_client.agents.update_agent.assert_not_called()
        # But success message should still be logged (with 0 servers)
        self.mock_logger.info.assert_called_with(
            "Successfully configured 0 MCP tool servers for agent"
        )
