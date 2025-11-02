# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Unit tests for the real MCPServerConfig model from the tooling library.
Tests the actual validation logic and dataclass behavior.
"""

import pytest
from microsoft_agents_a365.tooling.models.mcp_server_config import MCPServerConfig


class TestRealMCPServerConfig:
    """Test class for the actual MCPServerConfig dataclass from the tooling library."""

    def test_valid_initialization(self):
        """Test successful initialization with valid parameters."""
        # Arrange
        server_name = "mail_server"
        unique_name = "mcp_mail_tools"

        # Act
        config = MCPServerConfig(mcp_server_name=server_name, mcp_server_unique_name=unique_name)

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
        """Test initialization succeeds with whitespace-only server name (truthy value)."""
        # Arrange & Act
        config = MCPServerConfig(mcp_server_name="   ", mcp_server_unique_name="valid_unique_name")

        # Assert
        assert config.mcp_server_name == "   "
        assert config.mcp_server_unique_name == "valid_unique_name"

    def test_initialization_with_whitespace_unique_name_succeeds(self):
        """Test initialization succeeds with whitespace-only unique name (truthy value)."""
        # Arrange & Act
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
            hash(config1)

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

    def test_post_init_validation_called(self):
        """Test that __post_init__ validation is properly called during initialization."""
        # This test ensures that the validation logic is triggered during object creation

        # Test that valid initialization works
        config = MCPServerConfig(mcp_server_name="valid", mcp_server_unique_name="valid")
        assert config.mcp_server_name == "valid"

        # Test that validation prevents invalid objects from being created
        with pytest.raises(ValueError):
            MCPServerConfig(mcp_server_name="", mcp_server_unique_name="valid")

    def test_dataclass_properties(self):
        """Test that MCPServerConfig has expected dataclass properties."""
        # Arrange
        config = MCPServerConfig(mcp_server_name="test", mcp_server_unique_name="test")

        # Act & Assert
        # Test that it's a dataclass with the expected fields
        assert hasattr(config, "mcp_server_name")
        assert hasattr(config, "mcp_server_unique_name")
        assert hasattr(config, "__post_init__")

        # Test field annotations exist
        annotations = MCPServerConfig.__annotations__
        assert "mcp_server_name" in annotations
        assert "mcp_server_unique_name" in annotations
        assert annotations["mcp_server_name"] == str
        assert annotations["mcp_server_unique_name"] == str
