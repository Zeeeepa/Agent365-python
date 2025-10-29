# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Agent 365 Tooling Agent Framework Extensions

Agent Framework specific tools and services for AI agent development.
Provides Agent Framework-specific implementations and utilities for
building agents with Microsoft Agent Framework capabilities.

Main Service:
- McpToolRegistrationService: Add MCP tool servers to Agent Framework agents
"""

__version__ = "1.0.0"

# Import services
from .services import (
    McpToolRegistrationService,
)

__all__ = [
    "McpToolRegistrationService",
]
