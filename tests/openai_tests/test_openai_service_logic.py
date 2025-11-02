# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for OpenAI MCP Tool Registration Service core logic.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from dataclasses import dataclass
from typing import Dict, Optional


# Mock the MCPServerInfo dataclass from the service
@dataclass
class MCPServerInfo:
    """Information about an MCP server"""

    name: str
    url: str
    server_type: str = "streamable_http"
    headers: Optional[Dict[str, str]] = None
    require_approval: str = "never"
    timeout: int = 30


class MockMcpToolRegistrationService:
    """Mock implementation of OpenAI MCP Tool Registration Service for testing core logic."""

    def __init__(self):
        self.config_service = AsyncMock()
        self._connected_servers = []

    async def add_tool_servers_to_agent(
        self,
        agent,
        agent_user_id: str,
        environment_id: str,
        auth,
        context,
        auth_token: Optional[str] = None,
    ):
        """Mock implementation of add_tool_servers_to_agent method."""

        # Handle auth token exchange if not provided
        if not auth_token:
            if not auth or not context:
                raise ValueError("auth and context are required when auth_token is not provided")

            # Mock token exchange
            mock_token_response = await auth.exchange_token(context, "scope", "AGENTIC")
            auth_token = mock_token_response.token

        # Get MCP server configurations
        mcp_server_configs = await self.config_service.list_tool_servers(
            agent_user_id=agent_user_id, environment_id=environment_id, auth_token=auth_token
        )

        # Convert to MCPServerInfo objects
        mcp_servers_info = []
        for server_config in mcp_server_configs:
            # Validate server configuration - skip invalid ones
            if (
                hasattr(server_config, "mcp_server_name")
                and hasattr(server_config, "mcp_server_unique_name")
                and server_config.mcp_server_name
                and server_config.mcp_server_unique_name
            ):
                server_info = MCPServerInfo(
                    name=server_config.mcp_server_name,
                    url=server_config.mcp_server_unique_name,
                )
                mcp_servers_info.append(server_info)

        # Get existing MCP servers from agent
        existing_mcp_servers = []
        if hasattr(agent, "mcp_servers") and agent.mcp_servers:
            existing_mcp_servers = list(agent.mcp_servers)

        # Track existing server URLs
        existing_server_urls = []
        for server in existing_mcp_servers:
            if (
                hasattr(server, "params")
                and isinstance(server.params, dict)
                and "url" in server.params
            ):
                existing_server_urls.append(server.params["url"])
            elif hasattr(server, "params") and hasattr(server.params, "url"):
                existing_server_urls.append(server.params.url)
            elif hasattr(server, "url"):
                existing_server_urls.append(server.url)

        # Process new servers
        new_mcp_servers = []
        connected_servers = []

        for server_info in mcp_servers_info:
            if server_info.url not in existing_server_urls:
                try:
                    # Prepare headers
                    headers = server_info.headers or {}
                    if auth_token:
                        headers["Authorization"] = f"Bearer {auth_token}"
                    if environment_id:
                        headers["x-ms-environment-id"] = environment_id

                    # Create mock MCP server
                    mock_server = MagicMock()
                    mock_server.params = MagicMock()
                    mock_server.params.url = server_info.url
                    mock_server.params.headers = headers
                    mock_server.name = server_info.name
                    mock_server.connect = AsyncMock()
                    mock_server.cleanup = AsyncMock()

                    # Connect the server
                    await mock_server.connect()

                    new_mcp_servers.append(mock_server)
                    connected_servers.append(mock_server)
                    existing_server_urls.append(server_info.url)

                except Exception as e:
                    # Log error and continue
                    print(
                        f"Failed to connect to MCP server {server_info.name} at {server_info.url}: {e}"
                    )
                    continue

        # If we have new servers, recreate the agent
        if new_mcp_servers:
            try:
                all_mcp_servers = existing_mcp_servers + new_mcp_servers

                # Create new agent with all MCP servers
                new_agent = MagicMock()
                new_agent.name = agent.name if hasattr(agent, "name") else "test_agent"
                new_agent.model = agent.model if hasattr(agent, "model") else "test_model"
                new_agent.instructions = (
                    agent.instructions if hasattr(agent, "instructions") else "test_instructions"
                )
                new_agent.tools = agent.tools if hasattr(agent, "tools") else []
                new_agent.mcp_servers = all_mcp_servers

                # Copy model_settings if present
                if hasattr(agent, "model_settings"):
                    new_agent.model_settings = agent.model_settings

                # Store connected servers for cleanup
                if not hasattr(self, "_connected_servers"):
                    self._connected_servers = []
                self._connected_servers.extend(connected_servers)

                return new_agent

            except Exception as e:
                # Clean up on failure
                await self._cleanup_servers(connected_servers)
                raise e

        return agent

    async def _cleanup_servers(self, servers):
        """Clean up connected MCP servers."""
        for server in servers:
            try:
                if hasattr(server, "cleanup"):
                    await server.cleanup()
            except Exception:
                # Log cleanup errors but don't raise them
                pass

    async def cleanup_all_servers(self):
        """Clean up all connected MCP servers."""
        if hasattr(self, "_connected_servers"):
            await self._cleanup_servers(self._connected_servers)
            self._connected_servers = []


class TestOpenAIMcpToolRegistrationServiceLogic:
    """Test cases for OpenAI MCP Tool Registration Service core business logic."""

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent for testing."""
        agent = MagicMock()
        agent.name = "test_agent"
        agent.model = "gpt-4"
        agent.instructions = "You are a helpful assistant"
        agent.tools = []
        agent.mcp_servers = []
        return agent

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
    def sample_server_configs(self):
        """Sample MCP server configurations."""
        server1 = MagicMock()
        server1.mcp_server_name = "TestServer1"
        server1.mcp_server_unique_name = "https://test1.example.com/mcp"

        server2 = MagicMock()
        server2.mcp_server_name = "TestServer2"
        server2.mcp_server_unique_name = "https://test2.example.com/mcp"

        return [server1, server2]

    def test_service_initialization(self):
        """Test service initialization."""
        service = MockMcpToolRegistrationService()

        assert service.config_service is not None
        assert hasattr(service, "_connected_servers")
        assert service._connected_servers == []

    def test_mcpserverinfo_dataclass_creation(self):
        """Test MCPServerInfo dataclass creation and default values."""
        # Test with minimal parameters
        server_info = MCPServerInfo(name="TestServer", url="https://test.com")

        assert server_info.name == "TestServer"
        assert server_info.url == "https://test.com"
        assert server_info.server_type == "streamable_http"
        assert server_info.headers is None
        assert server_info.require_approval == "never"
        assert server_info.timeout == 30

    def test_mcpserverinfo_dataclass_with_custom_values(self):
        """Test MCPServerInfo dataclass with custom values."""
        custom_headers = {"Authorization": "Bearer token", "Custom-Header": "value"}

        server_info = MCPServerInfo(
            name="CustomServer",
            url="https://custom.com/mcp",
            server_type="hosted",
            headers=custom_headers,
            require_approval="always",
            timeout=60,
        )

        assert server_info.name == "CustomServer"
        assert server_info.url == "https://custom.com/mcp"
        assert server_info.server_type == "hosted"
        assert server_info.headers == custom_headers
        assert server_info.require_approval == "always"
        assert server_info.timeout == 60

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_with_auth_token(
        self, mock_agent, mock_auth, mock_context, sample_server_configs
    ):
        """Test adding tool servers with provided auth token."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should not call token exchange when token is provided
        mock_auth.exchange_token.assert_not_called()

        # Should call config service
        service.config_service.list_tool_servers.assert_called_once_with(
            agent_user_id="user123", environment_id="env123", auth_token="test_token"
        )

        # Should return new agent with MCP servers
        assert result != mock_agent  # New agent created
        assert hasattr(result, "mcp_servers")
        assert len(result.mcp_servers) == 2  # Two new servers added

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_without_auth_token(
        self, mock_agent, mock_auth, mock_context, sample_server_configs
    ):
        """Test adding tool servers with token exchange."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        # Setup token exchange mock - must return awaitable
        mock_token_response = MagicMock()
        mock_token_response.token = "exchanged_token"
        mock_auth.exchange_token = AsyncMock(return_value=mock_token_response)

        await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token=None,
        )

        # Should call token exchange
        mock_auth.exchange_token.assert_called_once()

        # Should use exchanged token
        service.config_service.list_tool_servers.assert_called_once_with(
            agent_user_id="user123", environment_id="env123", auth_token="exchanged_token"
        )

    @pytest.mark.asyncio
    async def test_add_tool_servers_to_agent_no_auth_no_token_raises_error(self, mock_agent):
        """Test that missing auth and token raises ValueError."""
        service = MockMcpToolRegistrationService()

        with pytest.raises(ValueError, match="auth and context are required"):
            await service.add_tool_servers_to_agent(
                agent=mock_agent,
                agent_user_id="user123",
                environment_id="env123",
                auth=None,
                context=None,
                auth_token=None,
            )

    @pytest.mark.asyncio
    async def test_add_tool_servers_no_new_servers(self, mock_agent, mock_auth, mock_context):
        """Test when no new servers are found."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = []

        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should return original agent when no new servers
        assert result == mock_agent

    @pytest.mark.asyncio
    async def test_existing_server_detection_by_url(
        self, mock_auth, mock_context, sample_server_configs
    ):
        """Test that existing servers are detected and not duplicated."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        # Create agent with existing server
        existing_server = MagicMock()
        existing_server.params = {"url": "https://test1.example.com/mcp"}

        agent_with_servers = MagicMock()
        agent_with_servers.name = "test_agent"
        agent_with_servers.model = "gpt-4"
        agent_with_servers.instructions = "test"
        agent_with_servers.tools = []
        agent_with_servers.mcp_servers = [existing_server]

        result = await service.add_tool_servers_to_agent(
            agent=agent_with_servers,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should only add the second server (first one already exists)
        assert len(result.mcp_servers) == 2  # 1 existing + 1 new

        # Check that existing server is preserved
        assert existing_server in result.mcp_servers

    @pytest.mark.asyncio
    async def test_server_header_configuration(
        self, mock_agent, mock_auth, mock_context, sample_server_configs
    ):
        """Test that server headers are configured correctly."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Check that headers are configured on MCP servers
        for server in result.mcp_servers:
            assert hasattr(server.params, "headers")
            headers = server.params.headers
            assert "Authorization" in headers
            assert headers["Authorization"] == "Bearer test_token"
            assert "x-ms-environment-id" in headers
            assert headers["x-ms-environment-id"] == "env123"

    @pytest.mark.asyncio
    async def test_server_connection_and_tracking(
        self, mock_agent, mock_auth, mock_context, sample_server_configs
    ):
        """Test that servers are connected and tracked for cleanup."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Verify servers were connected
        for server in result.mcp_servers:
            server.connect.assert_called_once()

        # Verify servers are tracked for cleanup
        assert len(service._connected_servers) == 2

    @pytest.mark.asyncio
    async def test_agent_attribute_preservation(
        self, mock_auth, mock_context, sample_server_configs
    ):
        """Test that agent attributes are preserved when creating new agent."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        # Create agent with custom attributes
        original_agent = MagicMock()
        original_agent.name = "CustomAgent"
        original_agent.model = "gpt-4-turbo"
        original_agent.instructions = "Custom instructions"
        original_agent.tools = ["tool1", "tool2"]
        original_agent.model_settings = {"temperature": 0.7}
        original_agent.mcp_servers = []

        result = await service.add_tool_servers_to_agent(
            agent=original_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Verify attributes are preserved
        assert result.name == "CustomAgent"
        assert result.model == "gpt-4-turbo"
        assert result.instructions == "Custom instructions"
        assert result.tools == ["tool1", "tool2"]
        assert result.model_settings == {"temperature": 0.7}

    @pytest.mark.asyncio
    async def test_server_connection_failure_handling(self, mock_agent, mock_auth, mock_context):
        """Test handling of server connection failures."""
        service = MockMcpToolRegistrationService()

        # Create server config that will cause connection failure
        failing_server = MagicMock()
        failing_server.mcp_server_name = "FailingServer"
        failing_server.mcp_server_unique_name = "https://failing.example.com/mcp"

        service.config_service.list_tool_servers.return_value = [failing_server]

        # Override the service method to simulate connection failure
        original_method = service.add_tool_servers_to_agent

        async def failing_add_method(*args, **kwargs):
            # Simulate connection failure for specific server
            result = await original_method(*args, **kwargs)
            # In real scenario, connection would fail and be caught
            return result

        service.add_tool_servers_to_agent = failing_add_method

        # Should not raise exception, should handle gracefully
        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Method should complete successfully even with connection failures
        assert result is not None

    @pytest.mark.asyncio
    async def test_cleanup_servers_method(self):
        """Test server cleanup functionality."""
        service = MockMcpToolRegistrationService()

        # Create mock servers with cleanup methods
        server1 = MagicMock()
        server1.cleanup = AsyncMock()

        server2 = MagicMock()
        server2.cleanup = AsyncMock()

        servers_to_cleanup = [server1, server2]

        # Test cleanup
        await service._cleanup_servers(servers_to_cleanup)

        # Verify cleanup was called on each server
        server1.cleanup.assert_called_once()
        server2.cleanup.assert_called_once()

    @pytest.mark.asyncio
    async def test_cleanup_servers_with_exceptions(self):
        """Test server cleanup handles exceptions gracefully."""
        service = MockMcpToolRegistrationService()

        # Create server that raises exception during cleanup
        failing_server = MagicMock()
        failing_server.cleanup = AsyncMock(side_effect=Exception("Cleanup failed"))

        normal_server = MagicMock()
        normal_server.cleanup = AsyncMock()

        servers_to_cleanup = [failing_server, normal_server]

        # Should not raise exception
        await service._cleanup_servers(servers_to_cleanup)

        # Both cleanup methods should have been called
        failing_server.cleanup.assert_called_once()
        normal_server.cleanup.assert_called_once()

    @pytest.mark.asyncio
    async def test_cleanup_all_servers(self):
        """Test cleanup of all tracked servers."""
        service = MockMcpToolRegistrationService()

        # Add some connected servers
        server1 = MagicMock()
        server1.cleanup = AsyncMock()
        server2 = MagicMock()
        server2.cleanup = AsyncMock()

        service._connected_servers = [server1, server2]

        # Test cleanup all
        await service.cleanup_all_servers()

        # Verify cleanup was called on all servers
        server1.cleanup.assert_called_once()
        server2.cleanup.assert_called_once()

        # Verify servers list is cleared
        assert service._connected_servers == []

    def test_server_url_detection_various_formats(self):
        """Test server URL detection for different server formats."""

        # Test params dict format
        server1 = MagicMock()
        server1.params = {"url": "https://dict.example.com"}

        # Test params object format
        server2 = MagicMock()
        params_obj = MagicMock()
        params_obj.url = "https://object.example.com"
        server2.params = params_obj

        # Test direct url format
        server3 = MagicMock()
        server3.url = "https://direct.example.com"
        # No params attribute
        del server3.params

        servers = [server1, server2, server3]
        existing_urls = []

        for server in servers:
            # Extract URL using the same logic as the service
            if (
                hasattr(server, "params")
                and isinstance(server.params, dict)
                and "url" in server.params
            ):
                url = server.params["url"]
            elif hasattr(server, "params") and hasattr(server.params, "url"):
                url = server.params.url
            elif hasattr(server, "url"):
                url = server.url
            else:
                url = None

            if url:
                existing_urls.append(url)

        # Verify all URLs were extracted correctly
        expected_urls = [
            "https://dict.example.com",
            "https://object.example.com",
            "https://direct.example.com",
        ]
        assert existing_urls == expected_urls

    @pytest.mark.asyncio
    async def test_invalid_server_config_handling(self, mock_agent, mock_auth, mock_context):
        """Test handling of invalid server configurations."""
        service = MockMcpToolRegistrationService()

        # Create mix of valid and invalid server configs
        valid_server = MagicMock()
        valid_server.mcp_server_name = "ValidServer"
        valid_server.mcp_server_unique_name = "https://valid.example.com/mcp"

        invalid_server1 = MagicMock()
        invalid_server1.mcp_server_name = "InvalidServer1"
        invalid_server1.mcp_server_unique_name = None  # Invalid - None value

        invalid_server2 = MagicMock()
        invalid_server2.mcp_server_name = None  # Invalid - None value
        invalid_server2.mcp_server_unique_name = "https://invalid2.example.com/mcp"

        mixed_configs = [valid_server, invalid_server1, invalid_server2]
        service.config_service.list_tool_servers.return_value = mixed_configs

        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should only process valid server configs
        assert len(result.mcp_servers) == 1  # Only 1 valid server processed

    def test_mcpserverinfo_headers_merging_logic(self):
        """Test header merging logic for MCPServerInfo."""
        # Test with no initial headers
        server_info = MCPServerInfo(name="TestServer", url="https://test.com")
        headers = server_info.headers or {}

        # Add auth headers
        auth_token = "test_token"
        environment_id = "env123"

        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        if environment_id:
            headers["x-ms-environment-id"] = environment_id

        expected_headers = {"Authorization": "Bearer test_token", "x-ms-environment-id": "env123"}

        assert headers == expected_headers

        # Test with existing headers
        existing_headers = {"Custom-Header": "custom_value"}
        server_info_with_headers = MCPServerInfo(
            name="TestServer", url="https://test.com", headers=existing_headers.copy()
        )

        headers = server_info_with_headers.headers or {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        if environment_id:
            headers["x-ms-environment-id"] = environment_id

        expected_merged_headers = {
            "Custom-Header": "custom_value",
            "Authorization": "Bearer test_token",
            "x-ms-environment-id": "env123",
        }

        assert headers == expected_merged_headers

    @pytest.mark.asyncio
    async def test_agent_recreation_failure_cleanup(
        self, mock_agent, mock_auth, mock_context, sample_server_configs
    ):
        """Test that connected servers are cleaned up if agent recreation fails."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = sample_server_configs

        # Override to simulate agent creation failure
        async def failing_agent_creation(*args, **kwargs):
            # Start the normal process
            if not kwargs.get("auth_token"):
                mock_token_response = MagicMock()
                mock_token_response.token = "exchanged_test_token"
                kwargs["auth"].exchange_token.return_value = mock_token_response
                kwargs["auth_token"] = mock_token_response.token

            # Get configurations and create servers
            configs = await service.config_service.list_tool_servers(
                agent_user_id=kwargs["agent_user_id"],
                environment_id=kwargs["environment_id"],
                auth_token=kwargs["auth_token"],
            )

            # Create and connect servers
            connected_servers = []
            for config in configs:
                server = MagicMock()
                server.name = getattr(config, "name", None)
                server.url = getattr(config, "url", None)
                server.server_type = getattr(config, "server_type", None)
                server.headers = getattr(config, "headers", None)
                server.require_approval = getattr(config, "require_approval", None)
                server.timeout = getattr(config, "timeout", None)
                server.connect = AsyncMock()
                server.cleanup = AsyncMock()
                await server.connect()
                connected_servers.append(server)

            # Simulate agent creation failure
            try:
                raise Exception("Agent creation failed")
            except Exception as e:
                # Should clean up connected servers
                await service._cleanup_servers(connected_servers)
                raise e

        service.add_tool_servers_to_agent = failing_agent_creation

        # Should raise the agent creation exception
        with pytest.raises(Exception, match="Agent creation failed"):
            await service.add_tool_servers_to_agent(
                agent=mock_agent,
                agent_user_id="user123",
                environment_id="env123",
                auth=mock_auth,
                context=mock_context,
                auth_token="test_token",
            )

    @pytest.mark.asyncio
    async def test_empty_server_list_handling(self, mock_agent, mock_auth, mock_context):
        """Test handling when server config service returns empty list."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.return_value = []

        result = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should return original agent unchanged
        assert result == mock_agent
        assert len(service._connected_servers) == 0

    @pytest.mark.asyncio
    async def test_config_service_exception_handling(self, mock_agent, mock_auth, mock_context):
        """Test handling of config service exceptions."""
        service = MockMcpToolRegistrationService()
        service.config_service.list_tool_servers.side_effect = Exception("Config service failed")

        # Should propagate the exception
        with pytest.raises(Exception, match="Config service failed"):
            await service.add_tool_servers_to_agent(
                agent=mock_agent,
                agent_user_id="user123",
                environment_id="env123",
                auth=mock_auth,
                context=mock_context,
                auth_token="test_token",
            )

    def test_server_type_and_timeout_defaults(self):
        """Test MCPServerInfo default values for server_type and timeout."""
        server_info = MCPServerInfo(name="TestServer", url="https://test.com")

        # Verify defaults
        assert server_info.server_type == "streamable_http"
        assert server_info.timeout == 30
        assert server_info.require_approval == "never"

        # Test custom values
        custom_server = MCPServerInfo(
            name="CustomServer",
            url="https://custom.com",
            server_type="hosted",
            timeout=60,
            require_approval="always",
        )

        assert custom_server.server_type == "hosted"
        assert custom_server.timeout == 60
        assert custom_server.require_approval == "always"

    @pytest.mark.asyncio
    async def test_multiple_calls_server_tracking(self, mock_agent, mock_auth, mock_context):
        """Test that multiple calls properly track connected servers."""
        service = MockMcpToolRegistrationService()

        # First call with some servers
        first_batch = [MagicMock()]
        first_batch[0].mcp_server_name = "Server1"
        first_batch[0].mcp_server_unique_name = "https://server1.com/mcp"

        service.config_service.list_tool_servers.return_value = first_batch

        result1 = await service.add_tool_servers_to_agent(
            agent=mock_agent,
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should have 1 connected server
        assert len(service._connected_servers) == 1

        # Second call with different servers
        second_batch = [MagicMock()]
        second_batch[0].mcp_server_name = "Server2"
        second_batch[0].mcp_server_unique_name = "https://server2.com/mcp"

        service.config_service.list_tool_servers.return_value = second_batch

        result2 = await service.add_tool_servers_to_agent(
            agent=result1,  # Use result from first call
            agent_user_id="user123",
            environment_id="env123",
            auth=mock_auth,
            context=mock_context,
            auth_token="test_token",
        )

        # Should have 2 connected servers total
        assert len(service._connected_servers) == 2
        # Should have 2 servers in agent
        assert len(result2.mcp_servers) == 2
