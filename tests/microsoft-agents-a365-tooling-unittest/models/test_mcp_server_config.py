# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for MCPServerConfig model.
"""

import pytest
from dataclasses import dataclass
from typing import Optional


@dataclass
class MCPServerConfig:
    """Mock implementation of MCPServerConfig for testing core logic."""

    mcp_server_name: str
    mcp_server_unique_name: str

    def __post_init__(self):
        """Validate the configuration after initialization."""
        if not self.mcp_server_name or not self.mcp_server_name.strip():
            raise ValueError("mcp_server_name cannot be empty")
        if not self.mcp_server_unique_name or not self.mcp_server_unique_name.strip():
            raise ValueError("mcp_server_unique_name cannot be empty")


class TestMCPServerConfig:
    """Test class for MockMCPServerConfig dataclass."""

    def test_valid_initialization(self):
        """Test successful initialization with valid parameters."""
        # Arrange
        server_name = "mail_server"
        unique_name = "mcp_mail_tools"

        # Act
        config = MockMCPServerConfig(
            mcp_server_name=server_name, mcp_server_unique_name=unique_name
        )

        # Assert
        assert config.mcp_server_name == server_name
        assert config.mcp_server_unique_name == unique_name

    def test_initialization_with_empty_server_name_raises_error(self):
        """Test initialization fails with empty server name."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="mcp_server_name cannot be empty"):
            MCPServerConfig(mcp_server_name="", mcp_server_unique_name="valid_unique_name")

    def test_initialization_with_none_server_name_raises_error(self):
        """Test initialization fails with None server name."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="mcp_server_name cannot be empty"):
            MCPServerConfig(mcp_server_name=None, mcp_server_unique_name="valid_unique_name")

    def test_initialization_with_empty_unique_name_raises_error(self):
        """Test initialization fails with empty unique name."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="mcp_server_unique_name cannot be empty"):
            MCPServerConfig(mcp_server_name="valid_server_name", mcp_server_unique_name="")

    def test_initialization_with_none_unique_name_raises_error(self):
        """Test initialization fails with None unique name."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="mcp_server_unique_name cannot be empty"):
            MCPServerConfig(mcp_server_name="valid_server_name", mcp_server_unique_name=None)

    def test_initialization_with_whitespace_server_name_succeeds(self):
        """Test initialization succeeds with whitespace-only server name (implementation allows this)."""
        # Arrange & Act - The current implementation allows whitespace strings
        config = MCPServerConfig(mcp_server_name="   ", mcp_server_unique_name="valid_unique_name")

        # Assert
        assert config.mcp_server_name == "   "
        assert config.mcp_server_unique_name == "valid_unique_name"

    def test_initialization_with_whitespace_unique_name_succeeds(self):
        """Test initialization succeeds with whitespace-only unique name (implementation allows this)."""
        # Arrange & Act - The current implementation allows whitespace strings
        config = MCPServerConfig(mcp_server_name="valid_server_name", mcp_server_unique_name="   ")

        # Assert
        assert config.mcp_server_name == "valid_server_name"
        assert config.mcp_server_unique_name == "   "

    def test_equality_comparison(self):
        """Test equality comparison between MCPServerConfig instances."""
        # Arrange
        config1 = MCPServerConfig(mcp_server_name="server1", mcp_server_unique_name="unique1")
        config2 = MCPServerConfig(mcp_server_name="server1", mcp_server_unique_name="unique1")
        config3 = MCPServerConfig(mcp_server_name="server2", mcp_server_unique_name="unique1")

        # Act & Assert
        assert config1 == config2
        assert config1 != config3
        assert config2 != config3

    def test_string_representation(self):
        """Test string representation of MCPServerConfig."""
        # Arrange
        config = MCPServerConfig(
            mcp_server_name="test_server", mcp_server_unique_name="test_unique"
        )

        # Act
        str_repr = str(config)

        # Assert
        assert "test_server" in str_repr
        assert "test_unique" in str_repr

    def test_hash_functionality_not_supported(self):
        """Test that MCPServerConfig instances cannot be used as dictionary keys (dataclass not frozen)."""
        # Arrange
        config1 = MCPServerConfig(mcp_server_name="server1", mcp_server_unique_name="unique1")

        # Act & Assert - Dataclass without frozen=True is not hashable
        with pytest.raises(TypeError, match="unhashable type"):
            config_dict = {config1: "value1"}

    def test_field_assignment_after_creation(self):
        """Test that fields can be modified after creation."""
        # Arrange
        config = MCPServerConfig(
            mcp_server_name="original_server", mcp_server_unique_name="original_unique"
        )

        # Act
        config.mcp_server_name = "modified_server"
        config.mcp_server_unique_name = "modified_unique"

        # Assert
        assert config.mcp_server_name == "modified_server"
        assert config.mcp_server_unique_name == "modified_unique"

    def test_with_special_characters_in_names(self):
        """Test initialization with special characters in names."""
        # Arrange & Act
        config = MCPServerConfig(
            mcp_server_name="server-with_special.chars@domain",
            mcp_server_unique_name="unique/path/with%20spaces",
        )

        # Assert
        assert config.mcp_server_name == "server-with_special.chars@domain"
        assert config.mcp_server_unique_name == "unique/path/with%20spaces"

    def test_with_unicode_characters(self):
        """Test initialization with Unicode characters."""
        # Arrange & Act
        config = MCPServerConfig(mcp_server_name="服务器名称", mcp_server_unique_name="مخدم_فريد")

        # Assert
        assert config.mcp_server_name == "服务器名称"
        assert config.mcp_server_unique_name == "مخدم_فريد"

    def test_with_long_strings(self):
        """Test initialization with very long strings."""
        # Arrange
        long_server_name = "a" * 1000
        long_unique_name = "b" * 1000

        # Act
        config = MCPServerConfig(
            mcp_server_name=long_server_name, mcp_server_unique_name=long_unique_name
        )

        # Assert
        assert config.mcp_server_name == long_server_name
        assert config.mcp_server_unique_name == long_unique_name
        assert len(config.mcp_server_name) == 1000
        assert len(config.mcp_server_unique_name) == 1000
