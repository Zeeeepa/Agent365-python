# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
MCP Tool Registration Service implementation for Agent Framework.

This module provides the concrete implementation of the MCP (Model Context Protocol)
tool registration service that integrates with Agent Framework to add MCP tool
servers to agents.
"""

# Standard library imports
import logging
from typing import Optional, List, Any

# Third-party imports
from azure.identity import DefaultAzureCredential

# Agent Framework imports
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient
from agent_framework.azure import AzureOpenAIChatClient

# Local imports from tooling package
from microsoft_agents_a365.tooling.services.mcp_tool_server_configuration_service import (
    McpToolServerConfigurationService,
)
from microsoft_agents_a365.tooling.models import MCPServerConfig
from microsoft_agents_a365.tooling.utils.constants import Constants


class McpToolRegistrationService:
    """
    Provides MCP tool registration services for Agent Framework agents.

    This service handles registration and management of MCP (Model Context Protocol)
    tool servers with Agent Framework agents. It provides seamless integration
    between MCP servers and Microsoft Agent Framework.

    Features:
    - Automatic MCP server discovery and configuration
    - Azure identity integration with DefaultAzureCredential
    - Tool definitions and resources management
    - Support for both development (ToolingManifest.json) and production (gateway API) scenarios
    - Comprehensive error handling and logging

    Example:
        >>> service = McpToolRegistrationService()
        >>> agent = await service.add_tool_servers_to_agent(
        ...     chat_client=chat_client,
        ...     agent_instructions="You are a helpful assistant.",
        ...     initial_tools=[],
        ...     agent_user_id="user-123",
        ...     environment_id="prod",
        ...     auth_token="your-token"
        ... )
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        credential: Optional["DefaultAzureCredential"] = None,
    ):
        """
        Initialize the MCP Tool Registration Service for Agent Framework.

        Args:
            logger: Logger instance for logging operations.
            credential: Azure credential for authentication. If None, DefaultAzureCredential will be used.
        """
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._credential = credential or DefaultAzureCredential()
        self._mcp_server_configuration_service = McpToolServerConfigurationService(
            logger=self._logger
        )

    # ============================================================================
    # Public Methods - Main Entry Points
    # ============================================================================

    async def add_tool_servers_to_agent(
        self,
        chat_client: Any,  # OpenAIChatClient or AzureOpenAIChatClient
        agent_instructions: str,
        initial_tools: List[Any],
        agent_user_id: str,
        environment_id: str,
        auth_token: Optional[str] = None,
    ) -> "ChatAgent":
        """
        Add new MCP servers to the agent by creating a new ChatAgent instance.

        Note: Due to Agent Framework design, MCP tools must be set during
        ChatAgent creation. If new tools are found, this method creates a new ChatAgent
        instance with all tools (existing + new) properly initialized.

        Args:
            chat_client: The configured chat client (OpenAIChatClient or AzureOpenAIChatClient).
            agent_instructions: The agent instructions.
            initial_tools: The existing tools to add servers to.
            agent_user_id: Agent User ID for the agent.
            environment_id: Environment ID for the environment.
            auth_token: Authentication token to access the MCP servers.

        Returns:
            New ChatAgent instance with all MCP tools, or agent with original tools if no new servers.

        Raises:
            ValueError: If chat_client is None or auth_token is invalid.
            Exception: If there's an error during MCP tool registration.
        """
        if chat_client is None:
            raise ValueError("chat_client cannot be None")

        if not auth_token or auth_token.strip() == "":
            raise ValueError("Auth token cannot be null or empty.")

        try:
            # Step 2: Now update agent by adding MCP tools
            updated_tools = []

            # Keep any existing tools that were passed in
            updated_tools.extend(initial_tools)

            # Get MCP tool server configurations
            servers = await self._mcp_server_configuration_service.list_tool_servers(
                agent_user_id, environment_id, auth_token
            )

            # Retrieve MCP tools from all configured servers
            for server in servers:
                try:
                    mcp_tools = await self._get_tools(server, environment_id, auth_token)
                    # Add the MCP tools
                    updated_tools.extend(mcp_tools)

                    self._logger.info(
                        f"Successfully loaded {len(mcp_tools)} tools from MCP server '{server.mcp_server_name}'"
                    )
                except Exception as ex:
                    self._logger.error(
                        f"Failed to load tools from MCP server '{server.mcp_server_name}': {ex}"
                    )

            self._logger.info(
                f"Loaded {len(updated_tools)} MCP tools for agent {agent_user_id} in environment {environment_id}"
            )

            # Create ChatAgent with updated tools (since ChatAgent is immutable)
            agent_with_tools = ChatAgent(
                chat_client=chat_client, instructions=agent_instructions, tools=updated_tools
            )

            # Return the enhanced agent
            return agent_with_tools

        except Exception as ex:
            self._logger.error(
                f"Failed to add MCP tool servers for agent {agent_user_id} in environment {environment_id}: {ex}"
            )
            raise

    # ============================================================================
    # Private Methods - Implementation Details
    # ============================================================================

    async def _get_tools(
        self, server: MCPServerConfig, environment_id: str, auth_token: str
    ) -> List[Any]:
        """
        Get tools from a specific MCP server.

        Args:
            server: MCP server configuration.
            environment_id: Environment ID for the environment.
            auth_token: Authentication token for the MCP server.

        Returns:
            List of tools from the MCP server.
        """
        if not server.mcp_server_name or not server.mcp_server_unique_name:
            self._logger.warning(
                f"Skipping invalid MCP server config: Name='{server.mcp_server_name}', Url='{server.mcp_server_unique_name}'"
            )
            return []

        try:
            # Create headers for MCP server authentication
            headers = {
                Constants.Headers.AUTHORIZATION: f"{Constants.Headers.BEARER_PREFIX} {auth_token}",
                Constants.Headers.ENVIRONMENT_ID: environment_id,
            }

            # Create MCP plugin using Agent Framework
            plugin = MCPStreamableHTTPTool(
                name=server.mcp_server_name,
                url=server.mcp_server_unique_name,
                headers=headers or None,
            )

            # Get tools from the MCP plugin
            tools = await plugin.get_tools()

            self._logger.info(
                f"Retrieved {len(tools)} tools from MCP server {server.mcp_server_name}"
            )
            return tools

        except Exception as ex:
            self._logger.error(
                f"Failed to get tools from MCP server {server.mcp_server_name}: {ex}"
            )
            return []
