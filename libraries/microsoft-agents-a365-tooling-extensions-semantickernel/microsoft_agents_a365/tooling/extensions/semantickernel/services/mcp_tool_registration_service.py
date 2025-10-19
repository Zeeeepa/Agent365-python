# Copyright (c) Microsoft. All rights reserved.

"""
MCP Tool Registration Service implementation for Semantic Kernel.

This module provides the concrete implementation of the MCP (Model Context Protocol)
tool registration service that integrates with Semantic Kernel to add MCP tool
servers to agents.
"""

# Standard library imports
import logging
import os
import re
from typing import Any, Optional
from semantic_kernel import kernel as sk

# Third-party imports

# Local imports
from ...common.services.mcp_tool_server_configuration_service import (
    McpToolServerConfigurationService,
)
from ...common.models import MCPServerConfig
from ...common.utils.constants import Constants
from ...common.utils.utility import get_tools_mode

from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin


class McpToolRegistrationService:
    """
    Provides services related to tools in the Semantic Kernel.

    This service handles registration and management of MCP (Model Context Protocol)
    tool servers with Semantic Kernel agents.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        service_provider: Optional[Any] = None,
        mcp_server_configuration_service: Optional[McpToolServerConfigurationService] = None,
    ):
        """
        Initialize the MCP Tool Registration Service.

        Args:
            logger: Logger instance for logging operations.
            service_provider: Service provider for dependency injection.
            mcp_server_configuration_service: Service for MCP server configuration.
        """
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._service_provider = service_provider
        self._mcp_server_configuration_service = mcp_server_configuration_service

        # Store connected plugins to keep them alive
        self._connected_plugins = []

        # Enable debug logging if configured
        if os.getenv("MCP_DEBUG_LOGGING", "false").lower() == "true":
            self._logger.setLevel(logging.DEBUG)

        # Configure strict parameter validation (prevents dynamic property creation)
        self._strict_parameter_validation = (
            os.getenv("MCP_STRICT_PARAMETER_VALIDATION", "true").lower() == "true"
        )
        if self._strict_parameter_validation:
            self._logger.info(
                "🔒 Strict parameter validation enabled - only schema-defined parameters are allowed"
            )
        else:
            self._logger.info(
                "🔓 Strict parameter validation disabled - dynamic parameters are allowed"
            )

    # ============================================================================
    # Public Methods
    # ============================================================================

    async def add_tool_servers_to_agent(
        self, kernel: sk.Kernel, agent_user_id: str, environment_id: str, auth_token: str
    ) -> None:
        """
        Adds the A365 MCP Tool Servers to the specified kernel.

        Args:
            kernel: The Semantic Kernel instance to which the tools will be added.
            agent_user_id: Agent User ID for the agent.
            environment_id: Environment ID for the environment.
            auth_token: Authentication token to access the MCP servers.

        Raises:
            ValueError: If kernel is None or required parameters are invalid.
            Exception: If there's an error connecting to or configuring MCP servers.
        """
        self._validate_inputs(kernel, agent_user_id, environment_id, auth_token)

        if self._mcp_server_configuration_service is None:
            raise ValueError(
                "MCP server configuration service is required but was not provided during initialization"
            )

        # Get and process servers
        servers = await self._mcp_server_configuration_service.list_tool_servers(
            agent_user_id, environment_id, auth_token
        )
        self._logger.info(f"🔧 Adding MCP tools from {len(servers)} servers")

        # Get tools mode
        tools_mode = get_tools_mode()

        # Process each server (matching C# foreach pattern)
        for server in servers:
            try:
                if tools_mode == "HardCodedTools":
                    await self._add_hardcoded_tools_for_server(kernel, server)
                    continue

                headers = {}

                if tools_mode == "MockMCPServer":
                    # Mock server does not require bearer auth, but still forward environment id if available.
                    if environment_id:
                        headers[Constants.Headers.ENVIRONMENT_ID] = environment_id

                    if mock_auth_header := os.getenv("MOCK_MCP_AUTHORIZATION"):
                        headers[Constants.Headers.AUTHORIZATION] = mock_auth_header
                else:
                    headers = {
                        Constants.Headers.AUTHORIZATION: f"{Constants.Headers.BEARER_PREFIX} {auth_token}",
                        Constants.Headers.ENVIRONMENT_ID: environment_id,
                    }

                plugin = MCPStreamableHttpPlugin(
                    name=server.mcp_server_name,
                    url=server.mcp_server_unique_name,
                    headers=headers or None,
                )

                # Connect the plugin
                await plugin.connect()

                # Add plugin to kernel
                kernel.add_plugin(plugin, server.mcp_server_name)

                # Store reference to keep plugin alive throughout application lifecycle
                # By storing plugin references in _connected_plugins, we prevent Python's garbage collector from cleaning up the plugin objects
                # The connections remain active throughout the application lifecycle
                # Tools can be successfully invoked because their underlying connections are still alive
                self._connected_plugins.append(plugin)

                self._logger.info(
                    f"✅ Connected and added MCP plugin ({tools_mode}) for: {server.mcp_server_name}"
                )

            except Exception as e:
                self._logger.error(f"Failed to add tools from {server.mcp_server_name}: {str(e)}")

        self._logger.info("✅ Successfully configured MCP tool servers for the agent!")

    # ============================================================================
    # Private Methods - Input Validation & Processing
    # ============================================================================

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

    async def _add_hardcoded_tools_for_server(self, kernel: Any, server: MCPServerConfig) -> None:
        """Add hardcoded tools for a specific server (equivalent to C# hardcoded tool logic)."""
        server_name = server.mcp_server_name

        if server_name.lower() == "mcp_mailtools":
            # TODO: Implement hardcoded mail tools
            # kernel.plugins.add(KernelPluginFactory.create_from_type(HardCodedMailTools, server.mcp_server_name, self._service_provider))
            self._logger.info(f"Adding hardcoded mail tools for {server_name}")
        elif server_name.lower() == "mcp_sharepointtools":
            # TODO: Implement hardcoded SharePoint tools
            # kernel.plugins.add(KernelPluginFactory.create_from_type(HardCodedSharePointTools, server.mcp_server_name, self._service_provider))
            self._logger.info(f"Adding hardcoded SharePoint tools for {server_name}")
        elif server_name.lower() == "onedrivemcpserver":
            # TODO: Implement hardcoded OneDrive tools
            # kernel.plugins.add(KernelPluginFactory.create_from_type(HardCodedOneDriveTools, server.mcp_server_name, self._service_provider))
            self._logger.info(f"Adding hardcoded OneDrive tools for {server_name}")
        elif server_name.lower() == "wordmcpserver":
            # TODO: Implement hardcoded Word tools
            # kernel.plugins.add(KernelPluginFactory.create_from_type(HardCodedWordTools, server.mcp_server_name, self._service_provider))
            self._logger.info(f"Adding hardcoded Word tools for {server_name}")
        else:
            self._logger.warning(f"No hardcoded tools available for server: {server_name}")

    # ============================================================================
    # Private Methods - Kernel Function Creation
    # ============================================================================

    def _get_plugin_name_from_server_name(self, server_name: str) -> str:
        """Generate a clean plugin name from server name."""
        clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", server_name)
        return f"{clean_name}Tools"

    # ============================================================================
    # Cleanup Methods
    # ============================================================================

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
