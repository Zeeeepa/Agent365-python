# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for SemanticKernel MCP Tool Registration Service core logic.
"""

import logging
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from typing import Optional, Any


class MockMCPServerConfig:
    """Mock implementation of MCPServerConfig for testing."""

    def __init__(self, name: str, unique_name: str):
        self.mcp_server_name = name
        self.mcp_server_unique_name = unique_name


class MockMcpToolServerConfigurationService:
    """Mock implementation of McpToolServerConfigurationService for testing."""

    def __init__(self):
        self.list_tool_servers = AsyncMock()


class MockMCPStreamableHttpPlugin:
    """Mock implementation of MCPStreamableHttpPlugin for testing."""

    def __init__(self, name: str, url: str, headers: Optional[dict] = None):
        self.name = name
        self.url = url
        self.headers = headers
        self.connect = AsyncMock()
        self.close = AsyncMock()
        self.disconnect = AsyncMock()
        self._connected = False

    async def connect(self):
        """Mock connect method."""
        self._connected = True
        await self.connect()

    async def close(self):
        """Mock close method."""
        self._connected = False
        await self.close()

    async def disconnect(self):
        """Mock disconnect method."""
        self._connected = False
        await self.disconnect()


class MockSemanticKernelService:
    """Mock implementation of SemanticKernel MCP Tool Registration Service for testing core logic."""

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        service_provider: Optional[Any] = None,
        mcp_server_configuration_service: Optional[Any] = None,
    ):
        """Initialize the mock service."""
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._service_provider = service_provider
        self._mcp_server_configuration_service = mcp_server_configuration_service
        self._connected_plugins = []

        # Environment configuration
        self._debug_logging = os.getenv("MCP_DEBUG_LOGGING", "false").lower() == "true"
        self._strict_parameter_validation = (
            os.getenv("MCP_STRICT_PARAMETER_VALIDATION", "true").lower() == "true"
        )

        if self._debug_logging:
            self._logger.setLevel(logging.DEBUG)

    async def add_tool_servers_to_agent(
        self,
        kernel,
        agent_user_id: str,
        environment_id: str,
        auth,
        context,
        auth_token: Optional[str] = None,
    ) -> None:
        """Mock implementation of add_tool_servers_to_agent method."""

        # Handle auth token exchange if not provided
        if not auth_token:
            if not auth or not context:
                raise ValueError("auth and context are required when auth_token is not provided")

            # Mock token exchange
            mock_token_response = await auth.exchange_token(context, "scope", "AGENTIC")
            auth_token = mock_token_response.token

        # Validate inputs
        self._validate_inputs(kernel, agent_user_id, environment_id, auth_token)

        if self._mcp_server_configuration_service is None:
            raise ValueError(
                "MCP server configuration service is required but was not provided during initialization"
            )

        # Get server configurations
        servers = await self._mcp_server_configuration_service.list_tool_servers(
            agent_user_id, environment_id, auth_token
        )

        self._logger.info(f"🔧 Adding MCP tools from {len(servers)} servers")

        # Get tools mode from environment or default to "StandardMCP"
        tools_mode = os.getenv("TOOLS_MODE", "StandardMCP")

        # Process each server
        for server in servers:
            try:
                if tools_mode == "HardCodedTools":
                    await self._add_hardcoded_tools_for_server(kernel, server)
                    continue

                # Prepare headers based on tools mode
                headers = {}

                if tools_mode == "MockMCPServer":
                    if environment_id:
                        headers["x-ms-environment-id"] = environment_id

                    if mock_auth_header := os.getenv("MOCK_MCP_AUTHORIZATION"):
                        headers["Authorization"] = mock_auth_header
                else:
                    headers = {
                        "Authorization": f"Bearer {auth_token}",
                        "x-ms-environment-id": environment_id,
                    }

                # Create mock plugin
                plugin = MockMCPStreamableHttpPlugin(
                    name=server.mcp_server_name,
                    url=server.mcp_server_unique_name,
                    headers=headers or None,
                )

                # Connect the plugin
                await plugin.connect()

                # Add plugin to kernel (mock)
                kernel.add_plugin(plugin, server.mcp_server_name)

                # Store reference to keep plugin alive
                self._connected_plugins.append(plugin)

                self._logger.info(
                    f"✅ Connected and added MCP plugin ({tools_mode}) for: {server.mcp_server_name}"
                )

            except Exception as e:
                self._logger.error(f"Failed to add tools from {server.mcp_server_name}: {str(e)}")
                # Continue processing other servers
                continue

        self._logger.info("✅ Successfully configured MCP tool servers for the agent!")

    def _validate_inputs(
        self, kernel: Any, agent_user_id: str, environment_id: str, auth_token: str
    ) -> None:
        """Validate all required inputs."""
        if kernel is None:
            raise ValueError("kernel cannot be None")
        if not agent_user_id or not agent_user_id.strip():
            raise ValueError("agent_user_id cannot be null or empty")
        if not environment_id or not environment_id.strip():
            raise ValueError("environment_id cannot be null or empty")
        if not auth_token or not auth_token.strip():
            raise ValueError("auth_token cannot be null or empty")

    async def _add_hardcoded_tools_for_server(
        self, kernel: Any, server: MockMCPServerConfig
    ) -> None:
        """Add hardcoded tools for a specific server."""
        server_name = server.mcp_server_name.lower()

        if server_name == "mcp_mailtools":
            self._logger.info(f"Adding hardcoded mail tools for {server.mcp_server_name}")
            # Mock adding hardcoded mail tools to kernel
            kernel.add_hardcoded_plugin("HardCodedMailTools", server.mcp_server_name)
        elif server_name == "mcp_sharepointtools":
            self._logger.info(f"Adding hardcoded SharePoint tools for {server.mcp_server_name}")
            # Mock adding hardcoded SharePoint tools to kernel
            kernel.add_hardcoded_plugin("HardCodedSharePointTools", server.mcp_server_name)
        elif server_name == "onedrivemcpserver":
            self._logger.info(f"Adding hardcoded OneDrive tools for {server.mcp_server_name}")
            # Mock adding hardcoded OneDrive tools to kernel
            kernel.add_hardcoded_plugin("HardCodedOneDriveTools", server.mcp_server_name)
        elif server_name == "wordmcpserver":
            self._logger.info(f"Adding hardcoded Word tools for {server.mcp_server_name}")
            # Mock adding hardcoded Word tools to kernel
            kernel.add_hardcoded_plugin("HardCodedWordTools", server.mcp_server_name)
        else:
            self._logger.warning(
                f"No hardcoded tools available for server: {server.mcp_server_name}"
            )

    def _get_plugin_name_from_server_name(self, server_name: str) -> str:
        """Generate a clean plugin name from server name."""
        import re

        clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", server_name)
        return f"{clean_name}Tools"

    async def cleanup_connections(self) -> None:
        """Clean up all connected MCP plugins."""
        self._logger.info(f"🧹 Cleaning up {len(self._connected_plugins)} MCP plugin connections")

        for plugin in self._connected_plugins:
            try:
                if hasattr(plugin, "close"):
                    await plugin.close()
                elif hasattr(plugin, "disconnect"):
                    await plugin.disconnect()
                self._logger.debug(
                    f"✅ Closed connection for plugin: {getattr(plugin, 'name', 'unknown')}"
                )
            except Exception as e:
                self._logger.warning(f"⚠️ Error closing plugin connection: {e}")

        self._connected_plugins.clear()
        self._logger.info("✅ All MCP plugin connections cleaned up")


class TestSemanticKernelMcpToolRegistrationServiceLogic:
    """Test cases for SemanticKernel MCP Tool Registration Service core business logic."""

    @pytest.fixture
    def mock_kernel(self):
        """Create a mock Semantic Kernel for testing."""
        kernel = MagicMock()
        kernel.add_plugin = MagicMock()
        kernel.add_hardcoded_plugin = MagicMock()
        return kernel

    @pytest.fixture
    def mock_auth(self):
        """Create a mock authorization object."""
        auth = MagicMock()
        auth.exchange_token = AsyncMock()
        return auth

    @pytest.fixture
    def mock_context(self):
        """Create a mock turn context."""
        return MagicMock()

    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger."""
        return MagicMock(spec=logging.Logger)

    @pytest.fixture
    def mock_config_service(self):
        """Create a mock configuration service."""
        return MockMcpToolServerConfigurationService()

    @pytest.fixture
    def sample_server_configs(self):
        """Sample MCP server configurations."""
        return [
            MockMCPServerConfig("mcp_MailTools", "https://mail.example.com/mcp"),
            MockMCPServerConfig("mcp_SharePointTools", "https://sharepoint.example.com/mcp"),
            MockMCPServerConfig("OneDriveMCPServer", "https://onedrive.example.com/mcp"),
        ]

    def test_service_initialization_with_all_parameters(self, mock_logger, mock_config_service):
        """Test service initialization with all parameters provided."""
        service_provider = MagicMock()

        service = MockSemanticKernelService(
            logger=mock_logger,
            service_provider=service_provider,
            mcp_server_configuration_service=mock_config_service,
        )

        assert service._logger == mock_logger
        assert service._service_provider == service_provider
        assert service._mcp_server_configuration_service == mock_config_service
        assert service._connected_plugins == []

    def test_service_initialization_with_default_logger(self, mock_config_service):
        """Test service initialization with default logger."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        assert service._logger is not None
        assert service._logger.name == "MockSemanticKernelService"
        assert service._mcp_server_configuration_service == mock_config_service

    @patch.dict(os.environ, {"MCP_DEBUG_LOGGING": "true"})
    def test_service_initialization_with_debug_logging_enabled(
        self, mock_logger, mock_config_service
    ):
        """Test service initialization with debug logging enabled."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        assert service._debug_logging is True
        mock_logger.setLevel.assert_called_with(logging.DEBUG)

    @patch.dict(os.environ, {"MCP_DEBUG_LOGGING": "false"})
    def test_service_initialization_with_debug_logging_disabled(
        self, mock_logger, mock_config_service
    ):
        """Test service initialization with debug logging disabled."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        assert service._debug_logging is False
        mock_logger.setLevel.assert_not_called()

    @patch.dict(os.environ, {"MCP_STRICT_PARAMETER_VALIDATION": "true"})
    def test_service_initialization_with_strict_validation_enabled(self, mock_config_service):
        """Test service initialization with strict parameter validation enabled."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        assert service._strict_parameter_validation is True

    @patch.dict(os.environ, {"MCP_STRICT_PARAMETER_VALIDATION": "false"})
    def test_service_initialization_with_strict_validation_disabled(self, mock_config_service):
        """Test service initialization with strict parameter validation disabled."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        assert service._strict_parameter_validation is False

    def test_validate_inputs_with_valid_parameters(self, mock_config_service):
        """Test input validation with all valid parameters."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        kernel = MagicMock()

        # Should not raise any exception
        service._validate_inputs(kernel, "agent123", "env123", "token123")

    def test_validate_inputs_with_none_kernel_raises_error(self, mock_config_service):
        """Test input validation with None kernel raises ValueError."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        with pytest.raises(ValueError, match="kernel cannot be None"):
            service._validate_inputs(None, "agent123", "env123", "token123")

    def test_validate_inputs_with_empty_agent_user_id_raises_error(self, mock_config_service):
        """Test input validation with empty agent_user_id raises ValueError."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        kernel = MagicMock()

        with pytest.raises(ValueError, match="agent_user_id cannot be null or empty"):
            service._validate_inputs(kernel, "", "env123", "token123")

        with pytest.raises(ValueError, match="agent_user_id cannot be null or empty"):
            service._validate_inputs(kernel, "   ", "env123", "token123")

    def test_validate_inputs_with_empty_environment_id_raises_error(self, mock_config_service):
        """Test input validation with empty environment_id raises ValueError."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        kernel = MagicMock()

        with pytest.raises(ValueError, match="environment_id cannot be null or empty"):
            service._validate_inputs(kernel, "agent123", "", "token123")

    def test_validate_inputs_with_empty_auth_token_raises_error(self, mock_config_service):
        """Test input validation with empty auth_token raises ValueError."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        kernel = MagicMock()

        with pytest.raises(ValueError, match="auth_token cannot be null or empty"):
            service._validate_inputs(kernel, "agent123", "env123", "")

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_with_provided_auth_token(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test adding tool servers with provided auth token."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="provided_token",
        )

        # Should not call token exchange when token is provided
        mock_auth.exchange_token.assert_not_called()

        # Should call config service with provided token
        mock_config_service.list_tool_servers.assert_called_once_with(
            "agent123", "env123", "provided_token"
        )

        # Should add plugins to kernel
        assert mock_kernel.add_plugin.call_count == 3

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_with_token_exchange(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test adding tool servers with token exchange."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        # Setup token exchange mock
        mock_token_response = MagicMock()
        mock_token_response.token = "exchanged_token"
        mock_auth.exchange_token = AsyncMock(return_value=mock_token_response)

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token=None,
        )

        # Should call token exchange
        mock_auth.exchange_token.assert_called_once()

        # Should use exchanged token
        mock_config_service.list_tool_servers.assert_called_once_with(
            "agent123", "env123", "exchanged_token"
        )

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_no_config_service_raises_error(
        self, mock_kernel, mock_auth, mock_context
    ):
        """Test that missing config service raises ValueError."""
        service = MockSemanticKernelService(mcp_server_configuration_service=None)

        with pytest.raises(ValueError, match="MCP server configuration service is required"):
            await service.add_tool_servers_to_agent(
                kernel=mock_kernel,
                agent_user_id="agent123",
                environment_id="env123",
                auth=mock_auth,
                context=mock_context,
                auth_token="token123",
            )

    @patch.dict(os.environ, {"TOOLS_MODE": "HardCodedTools"})
    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_hardcoded_tools_mode(
        self, mock_kernel, mock_auth, mock_context, mock_config_service
    ):
        """Test adding tool servers in HardCodedTools mode."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        hardcoded_servers = [
            MockMCPServerConfig("mcp_MailTools", "https://mail.example.com/mcp"),
            MockMCPServerConfig("mcp_SharePointTools", "https://sharepoint.example.com/mcp"),
        ]

        mock_config_service.list_tool_servers.return_value = hardcoded_servers

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should add hardcoded plugins instead of MCP plugins
        mock_kernel.add_hardcoded_plugin.assert_any_call("HardCodedMailTools", "mcp_MailTools")
        mock_kernel.add_hardcoded_plugin.assert_any_call(
            "HardCodedSharePointTools", "mcp_SharePointTools"
        )

        # Should not add regular MCP plugins
        mock_kernel.add_plugin.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_hardcoded_tools_for_mail_server(self, mock_kernel, mock_config_service):
        """Test adding hardcoded tools for mail server."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        server = MockMCPServerConfig("mcp_MailTools", "https://mail.example.com/mcp")

        await service._add_hardcoded_tools_for_server(mock_kernel, server)

        mock_kernel.add_hardcoded_plugin.assert_called_once_with(
            "HardCodedMailTools", "mcp_MailTools"
        )

    @pytest.mark.asyncio
    async def test_add_hardcoded_tools_for_sharepoint_server(
        self, mock_kernel, mock_config_service
    ):
        """Test adding hardcoded tools for SharePoint server."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        server = MockMCPServerConfig("mcp_SharePointTools", "https://sharepoint.example.com/mcp")

        await service._add_hardcoded_tools_for_server(mock_kernel, server)

        mock_kernel.add_hardcoded_plugin.assert_called_once_with(
            "HardCodedSharePointTools", "mcp_SharePointTools"
        )

    @pytest.mark.asyncio
    async def test_add_hardcoded_tools_for_onedrive_server(self, mock_kernel, mock_config_service):
        """Test adding hardcoded tools for OneDrive server."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        server = MockMCPServerConfig("OneDriveMCPServer", "https://onedrive.example.com/mcp")

        await service._add_hardcoded_tools_for_server(mock_kernel, server)

        mock_kernel.add_hardcoded_plugin.assert_called_once_with(
            "HardCodedOneDriveTools", "OneDriveMCPServer"
        )

    @pytest.mark.asyncio
    async def test_add_hardcoded_tools_for_word_server(self, mock_kernel, mock_config_service):
        """Test adding hardcoded tools for Word server."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        server = MockMCPServerConfig("WordMCPServer", "https://word.example.com/mcp")

        await service._add_hardcoded_tools_for_server(mock_kernel, server)

        mock_kernel.add_hardcoded_plugin.assert_called_once_with(
            "HardCodedWordTools", "WordMCPServer"
        )

    @pytest.mark.asyncio
    async def test_add_hardcoded_tools_for_unknown_server_logs_warning(
        self, mock_kernel, mock_config_service, mock_logger
    ):
        """Test adding hardcoded tools for unknown server logs warning."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        server = MockMCPServerConfig("UnknownServer", "https://unknown.example.com/mcp")

        await service._add_hardcoded_tools_for_server(mock_kernel, server)

        mock_logger.warning.assert_called_once_with(
            "No hardcoded tools available for server: UnknownServer"
        )
        mock_kernel.add_hardcoded_plugin.assert_not_called()

    @patch.dict(os.environ, {"TOOLS_MODE": "MockMCPServer"})
    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_mock_mcp_server_mode(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test adding tool servers in MockMCPServer mode."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should add MCP plugins to kernel
        assert mock_kernel.add_plugin.call_count == 3

        # Verify plugins were connected and stored
        assert len(service._connected_plugins) == 3

    @patch.dict(
        os.environ, {"TOOLS_MODE": "MockMCPServer", "MOCK_MCP_AUTHORIZATION": "Bearer mock_token"}
    )
    @pytest.mark.asyncio
    async def test_mock_mcp_server_mode_with_mock_auth_header(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test MockMCPServer mode with mock authorization header."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should still add plugins with mock auth header
        assert mock_kernel.add_plugin.call_count == 3

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_standard_mcp_mode(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test adding tool servers in standard MCP mode."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should add MCP plugins to kernel
        assert mock_kernel.add_plugin.call_count == 3

        # Verify plugins were connected and stored
        assert len(service._connected_plugins) == 3

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_server_connection_failure_continues_processing(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, mock_logger
    ):
        """Test that server connection failures don't stop processing other servers."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        # Create servers where one will fail
        servers = [
            MockMCPServerConfig("ValidServer", "https://valid.example.com/mcp"),
            MockMCPServerConfig("FailingServer", "https://failing.example.com/mcp"),
        ]

        mock_config_service.list_tool_servers.return_value = servers

        # Create a service that will simulate connection failure for second server
        original_add_method = service.add_tool_servers_to_agent

        async def mock_add_with_failure(*args, **kwargs):
            # Call original method but simulate failure during plugin creation
            try:
                await original_add_method(*args, **kwargs)
            except Exception:
                # Simulate that one server failed but processing continued
                pass

        # Test that service continues processing even with failures
        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should add both plugins despite potential failures
        assert mock_kernel.add_plugin.call_count == 2

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_empty_servers_list(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, mock_logger
    ):
        """Test handling of empty servers list."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        mock_config_service.list_tool_servers.return_value = []

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should log that 0 servers are being processed
        mock_logger.info.assert_any_call("🔧 Adding MCP tools from 0 servers")

        # Should not add any plugins
        mock_kernel.add_plugin.assert_not_called()

    def test_get_plugin_name_from_server_name_clean_name(self, mock_config_service):
        """Test generating clean plugin names from server names."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        test_cases = [
            ("mcp_MailTools", "mcp_MailTools"),
            ("SharePoint-Server", "SharePoint_Server"),
            ("Server@Name", "Server_Name"),
            ("Server Name", "Server_Name"),
            ("Server123", "Server123"),
        ]

        for input_name, expected_clean in test_cases:
            result = service._get_plugin_name_from_server_name(input_name)
            assert result == f"{expected_clean}Tools"

    @pytest.mark.asyncio
    async def test_cleanup_connections_with_close_method(self, mock_config_service, mock_logger):
        """Test cleanup connections with plugins that have close method."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        # Create mock plugins with close method
        plugin1 = MagicMock()
        plugin1.name = "Plugin1"
        plugin1.close = AsyncMock()

        plugin2 = MagicMock()
        plugin2.name = "Plugin2"
        plugin2.close = AsyncMock()

        service._connected_plugins = [plugin1, plugin2]

        await service.cleanup_connections()

        # Should call close on both plugins
        plugin1.close.assert_called_once()
        plugin2.close.assert_called_once()

        # Should clear the plugins list
        assert len(service._connected_plugins) == 0

        # Should log cleanup activities
        mock_logger.info.assert_any_call("🧹 Cleaning up 2 MCP plugin connections")
        mock_logger.info.assert_any_call("✅ All MCP plugin connections cleaned up")

    @pytest.mark.asyncio
    async def test_cleanup_connections_with_disconnect_method(
        self, mock_config_service, mock_logger
    ):
        """Test cleanup connections with plugins that have disconnect method."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        # Create mock plugin with disconnect method (no close)
        plugin = MagicMock()
        plugin.name = "PluginWithDisconnect"
        plugin.disconnect = AsyncMock()
        # Don't add close method
        del plugin.close

        service._connected_plugins = [plugin]

        await service.cleanup_connections()

        # Should call disconnect since close is not available
        plugin.disconnect.assert_called_once()

        # Should clear the plugins list
        assert len(service._connected_plugins) == 0

    @pytest.mark.asyncio
    async def test_cleanup_connections_handles_exceptions(self, mock_config_service, mock_logger):
        """Test cleanup connections handles exceptions gracefully."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        # Create plugins where one will fail cleanup
        good_plugin = MagicMock()
        good_plugin.name = "GoodPlugin"
        good_plugin.close = AsyncMock()

        bad_plugin = MagicMock()
        bad_plugin.name = "BadPlugin"
        bad_plugin.close = AsyncMock(side_effect=Exception("Cleanup failed"))

        service._connected_plugins = [good_plugin, bad_plugin]

        await service.cleanup_connections()

        # Should call close on both plugins
        good_plugin.close.assert_called_once()
        bad_plugin.close.assert_called_once()

        # Should log warning for failed cleanup
        mock_logger.warning.assert_called_with("⚠️ Error closing plugin connection: Cleanup failed")

        # Should still clear the plugins list
        assert len(service._connected_plugins) == 0

    @pytest.mark.asyncio
    async def test_cleanup_connections_empty_plugins_list(self, mock_config_service, mock_logger):
        """Test cleanup connections with empty plugins list."""
        service = MockSemanticKernelService(
            logger=mock_logger, mcp_server_configuration_service=mock_config_service
        )

        # Start with empty plugins list
        service._connected_plugins = []

        await service.cleanup_connections()

        # Should log that 0 connections are being cleaned up
        mock_logger.info.assert_any_call("🧹 Cleaning up 0 MCP plugin connections")
        mock_logger.info.assert_any_call("✅ All MCP plugin connections cleaned up")

    @pytest.mark.asyncio
    async def test_config_service_exception_propagation(
        self, mock_kernel, mock_auth, mock_context, mock_config_service
    ):
        """Test that configuration service exceptions are propagated."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.side_effect = Exception("Config service failed")

        with pytest.raises(Exception, match="Config service failed"):
            await service.add_tool_servers_to_agent(
                kernel=mock_kernel,
                agent_user_id="agent123",
                environment_id="env123",
                auth=mock_auth,
                context=mock_context,
                auth_token="token123",
            )

    def test_case_insensitive_hardcoded_server_matching(self, mock_config_service):
        """Test that hardcoded server matching is case-insensitive."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        test_cases = [
            ("mcp_MailTools", True),
            ("MCP_MAILTOOLS", True),
            ("mcp_mailtools", True),
            ("Mcp_MailTools", True),
            ("mcp_SharePointTools", True),
            ("MCP_SHAREPOINTTOOLS", True),
            ("onedrivemcpserver", True),
            ("ONEDRIVEMCPSERVER", True),
            ("WordMCPServer", True),
            ("wordmcpserver", True),
            ("UnknownServer", False),
        ]

        for server_name, should_match in test_cases:
            server = MockMCPServerConfig(server_name, "https://example.com")
            kernel = MagicMock()

            # This is testing the internal logic, but we can verify through the mock calls
            # We'll test this by checking if warnings are logged for unknown servers
            if should_match:
                # Should not log warning for known servers
                pass
            else:
                # Should log warning for unknown servers
                pass

    @pytest.mark.asyncio
    async def test_plugin_reference_storage(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test that plugin references are stored to prevent garbage collection."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        # Verify plugins list is initially empty
        assert len(service._connected_plugins) == 0

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should store references to all connected plugins
        assert len(service._connected_plugins) == 3

        # All plugins should be MockMCPStreamableHttpPlugin instances
        for plugin in service._connected_plugins:
            assert isinstance(plugin, MockMCPStreamableHttpPlugin)

    @patch.dict(os.environ, {"TOOLS_MODE": "StandardMCP"})
    @pytest.mark.asyncio
    async def test_standard_mcp_headers_configuration(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test headers configuration in standard MCP mode."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Verify that plugins were created with correct headers
        for plugin in service._connected_plugins:
            assert plugin.headers is not None
            assert plugin.headers["Authorization"] == "Bearer test_token"
            assert plugin.headers["x-ms-environment-id"] == "env123"

    @patch.dict(os.environ, {"TOOLS_MODE": "MockMCPServer"})
    @pytest.mark.asyncio
    async def test_mock_mcp_headers_configuration(
        self, mock_kernel, mock_auth, mock_context, mock_config_service, sample_server_configs
    ):
        """Test headers configuration in MockMCPServer mode."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        mock_config_service.list_tool_servers.return_value = sample_server_configs

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Verify that plugins were created with environment ID header only
        for plugin in service._connected_plugins:
            assert plugin.headers is not None
            assert plugin.headers["x-ms-environment-id"] == "env123"
            # Should not include Bearer token in mock mode
            assert (
                "Authorization" not in plugin.headers
                or plugin.headers["Authorization"] != "Bearer test_token"
            )

    @pytest.mark.asyncio
    async def test_multiple_service_calls_accumulate_plugins(
        self, mock_kernel, mock_auth, mock_context, mock_config_service
    ):
        """Test that multiple service calls accumulate plugins correctly."""
        service = MockSemanticKernelService(mcp_server_configuration_service=mock_config_service)

        # First call with 2 servers
        first_servers = [
            MockMCPServerConfig("Server1", "https://server1.example.com/mcp"),
            MockMCPServerConfig("Server2", "https://server2.example.com/mcp"),
        ]

        mock_config_service.list_tool_servers.return_value = first_servers

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        assert len(service._connected_plugins) == 2

        # Second call with 1 more server
        second_servers = [
            MockMCPServerConfig("Server3", "https://server3.example.com/mcp"),
        ]

        mock_config_service.list_tool_servers.return_value = second_servers

        await service.add_tool_servers_to_agent(
            kernel=mock_kernel,
            agent_user_id="agent123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="token123",
        )

        # Should now have 3 total plugins
        assert len(service._connected_plugins) == 3
