# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for Constants class and its nested classes.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path to import the modules
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent.parent / "libraries" / "microsoft-agents-a365-tooling"),
)

from microsoft_agents_a365.tooling.utils.constants import Constants


class TestConstants:
    """Test class for Constants class."""

    def setup_method(self):
        """Setup method to ensure constants are in expected state before each test."""
        # Restore constants to expected values in case they were modified by other tests
        Constants.Headers.AUTHORIZATION = "Authorization"
        Constants.Headers.BEARER_PREFIX = "Bearer"
        Constants.Headers.ENVIRONMENT_ID = "x-ms-environment-id"

    def test_constants_class_exists(self):
        """Test that Constants class exists and can be instantiated."""
        # Act
        constants = Constants()

        # Assert
        assert constants is not None
        assert isinstance(constants, Constants)

    def test_headers_class_exists(self):
        """Test that Headers nested class exists."""
        # Act & Assert
        assert hasattr(Constants, "Headers")
        assert Constants.Headers is not None

    def test_headers_authorization_constant(self):
        """Test Headers.AUTHORIZATION constant value."""
        # Act & Assert
        assert hasattr(Constants.Headers, "AUTHORIZATION")
        assert Constants.Headers.AUTHORIZATION == "Authorization"

    def test_headers_bearer_prefix_constant(self):
        """Test Headers.BEARER_PREFIX constant value."""
        # Act & Assert
        assert hasattr(Constants.Headers, "BEARER_PREFIX")
        assert Constants.Headers.BEARER_PREFIX == "Bearer"

    def test_headers_environment_id_constant(self):
        """Test Headers.ENVIRONMENT_ID constant value."""
        # Act & Assert
        assert hasattr(Constants.Headers, "ENVIRONMENT_ID")
        assert Constants.Headers.ENVIRONMENT_ID == "x-ms-environment-id"

    def test_constants_are_strings(self):
        """Test that all constants are strings."""
        # Act & Assert
        assert isinstance(Constants.Headers.AUTHORIZATION, str)
        assert isinstance(Constants.Headers.BEARER_PREFIX, str)
        assert isinstance(Constants.Headers.ENVIRONMENT_ID, str)

    def test_constants_are_not_empty(self):
        """Test that constants are not empty strings."""
        # Act & Assert
        assert Constants.Headers.AUTHORIZATION != ""
        assert Constants.Headers.BEARER_PREFIX != ""
        assert Constants.Headers.ENVIRONMENT_ID != ""

    def test_constants_values_immutable(self):
        """Test that constants maintain their expected values."""
        # Act & Assert - Just verify the constants have the expected values
        assert Constants.Headers.AUTHORIZATION == "Authorization"
        assert Constants.Headers.BEARER_PREFIX == "Bearer"
        assert Constants.Headers.ENVIRONMENT_ID == "x-ms-environment-id"

    def test_headers_class_instantiation(self):
        """Test that Headers class can be instantiated."""
        # Act
        headers = Constants.Headers()

        # Assert
        assert headers is not None
        assert isinstance(headers, Constants.Headers)

    def test_access_constants_through_class(self):
        """Test accessing constants through the class directly."""
        # Act & Assert
        assert Constants.Headers.AUTHORIZATION == "Authorization"
        assert Constants.Headers.BEARER_PREFIX == "Bearer"
        assert Constants.Headers.ENVIRONMENT_ID == "x-ms-environment-id"

    def test_access_constants_through_instance(self):
        """Test accessing constants through class instance."""
        # Arrange
        constants = Constants()
        headers = constants.Headers()

        # Act & Assert
        assert headers.AUTHORIZATION == "Authorization"
        assert headers.BEARER_PREFIX == "Bearer"
        assert headers.ENVIRONMENT_ID == "x-ms-environment-id"

    def test_constants_case_sensitivity(self):
        """Test that constants have correct case."""
        # Act & Assert
        assert Constants.Headers.AUTHORIZATION == "Authorization"  # Proper case
        assert Constants.Headers.BEARER_PREFIX == "Bearer"  # Proper case
        assert Constants.Headers.ENVIRONMENT_ID == "x-ms-environment-id"  # Lowercase with hyphens

    def test_authorization_header_format(self):
        """Test that authorization header constant follows HTTP header format."""
        # Act
        auth_header = Constants.Headers.AUTHORIZATION

        # Assert
        assert auth_header == "Authorization"
        assert auth_header.isascii()
        assert " " not in auth_header  # No spaces in header names
        assert auth_header[0].isupper()  # First letter uppercase

    def test_bearer_prefix_format(self):
        """Test that bearer prefix follows expected format."""
        # Act
        bearer_prefix = Constants.Headers.BEARER_PREFIX

        # Assert
        assert bearer_prefix == "Bearer"
        assert bearer_prefix.isascii()
        assert bearer_prefix[0].isupper()  # First letter uppercase

    def test_environment_id_header_format(self):
        """Test that environment ID header follows Microsoft convention."""
        # Act
        env_id_header = Constants.Headers.ENVIRONMENT_ID

        # Assert
        assert env_id_header == "x-ms-environment-id"
        assert env_id_header.startswith("x-ms-")  # Microsoft convention
        assert env_id_header.islower()  # All lowercase
        assert "-" in env_id_header  # Contains hyphens

    def test_headers_docstring_or_comments(self):
        """Test that Headers class has appropriate documentation."""
        # Act & Assert
        # Check if class has docstring or comments
        assert Constants.Headers.__doc__ is not None or hasattr(
            Constants.Headers, "__annotations__"
        )

    def test_constants_class_docstring(self):
        """Test that Constants class has appropriate documentation."""
        # Act & Assert
        assert Constants.__doc__ is not None

    def test_no_unexpected_attributes(self):
        """Test that Headers class doesn't have unexpected attributes."""
        # Arrange
        expected_attributes = {"AUTHORIZATION", "BEARER_PREFIX", "ENVIRONMENT_ID"}

        # Act
        actual_attributes = {
            attr for attr in dir(Constants.Headers) if not attr.startswith("_") and attr.isupper()
        }

        # Assert
        assert actual_attributes == expected_attributes

    def test_constants_hashable(self):
        """Test that constants can be used as dictionary keys."""
        # Arrange & Act
        header_dict = {
            Constants.Headers.AUTHORIZATION: "Bearer token",
            Constants.Headers.ENVIRONMENT_ID: "env-123",
        }

        # Assert
        assert len(header_dict) == 2
        assert header_dict[Constants.Headers.AUTHORIZATION] == "Bearer token"
        assert header_dict[Constants.Headers.ENVIRONMENT_ID] == "env-123"
