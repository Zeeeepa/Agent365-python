# Copyright (c) Microsoft. All rights reserved.

"""
Kairo SDK Tooling OpenAI

Equivalent to Microsoft.Kairo.Sdk.Tooling.OpenAI

Tooling and utilities specifically for OpenAI framework integration.
Provides OpenAI-specific CLI tools and helper utilities.

This module includes sample implementations for:
- OpenAI Agent creation with MCP (Model Context Protocol) server support
- ToolService for dynamically adding MCP servers to agents
- Multiple MCP server type support (hosted, streamable HTTP, SSE, stdio)
- API integration patterns for MCP server discovery and configuration

Files:
- mcp_demo.py: Complete working demonstration
- sample_agent.py: Basic agent with MCP management
- advanced_tool_service.py: Advanced service with multiple server types
- tool_service_interface.py: Interface definitions and patterns
"""

__version__ = "1.0.0"
