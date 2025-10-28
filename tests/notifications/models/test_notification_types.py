# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for NotificationTypes enum
"""

import pytest
from microsoft_agents_a365.notifications.models.notification_types import NotificationTypes


class TestNotificationTypes:
    """Test cases for NotificationTypes enum"""

    def test_enum_values_exist(self):
        """Test that all expected enum values exist"""
        # Assert
        assert hasattr(NotificationTypes, 'EMAIL_NOTIFICATION')
        assert hasattr(NotificationTypes, 'WPX_COMMENT')
        assert hasattr(NotificationTypes, 'AGENT_LIFECYCLE')

    def test_enum_string_values(self):
        """Test that enum values have correct string representations"""
        # Assert
        assert NotificationTypes.EMAIL_NOTIFICATION == "emailNotification"
        assert NotificationTypes.WPX_COMMENT == "wpxComment"
        assert NotificationTypes.AGENT_LIFECYCLE == "agentLifecycle"

    def test_enum_is_string_based(self):
        """Test that NotificationTypes behaves as a string enum"""
        # Act & Assert
        assert isinstance(NotificationTypes.EMAIL_NOTIFICATION, str)
        assert isinstance(NotificationTypes.WPX_COMMENT, str)
        assert isinstance(NotificationTypes.AGENT_LIFECYCLE, str)

    def test_enum_string_equality(self):
        """Test equality comparison with string values"""
        # Assert
        assert NotificationTypes.EMAIL_NOTIFICATION == "emailNotification"
        assert NotificationTypes.WPX_COMMENT == "wpxComment"
        assert NotificationTypes.AGENT_LIFECYCLE == "agentLifecycle"
        
        # Test inequality
        assert NotificationTypes.EMAIL_NOTIFICATION != "wpxComment"
        assert NotificationTypes.WPX_COMMENT != "agentLifecycle"
        assert NotificationTypes.AGENT_LIFECYCLE != "emailNotification"

    def test_enum_string_formatting(self):
        """Test that enum values work in string formatting"""
        # Act
        email_string = f"Type: {NotificationTypes.EMAIL_NOTIFICATION}"
        wpx_string = f"Type: {NotificationTypes.WPX_COMMENT}"
        lifecycle_string = f"Type: {NotificationTypes.AGENT_LIFECYCLE}"

        # Assert
        assert email_string == "Type: NotificationTypes.EMAIL_NOTIFICATION"
        assert wpx_string == "Type: NotificationTypes.WPX_COMMENT"
        assert lifecycle_string == "Type: NotificationTypes.AGENT_LIFECYCLE"

    def test_enum_iteration(self):
        """Test iterating over all enum values"""
        # Act
        enum_values = list(NotificationTypes)
        enum_value_strings = [nt.value for nt in NotificationTypes]

        # Assert
        assert len(enum_values) == 3
        expected_values = {"emailNotification", "wpxComment", "agentLifecycle"}
        actual_values = set(enum_value_strings)
        assert actual_values == expected_values

    def test_enum_membership_check(self):
        """Test checking membership in enum"""
        # Act & Assert
        all_values = [nt.value for nt in NotificationTypes]
        
        assert "emailNotification" in all_values
        assert "wpxComment" in all_values
        assert "agentLifecycle" in all_values
        assert "invalidType" not in all_values
        assert "unknown" not in all_values

    def test_enum_creation_from_string_value(self):
        """Test creating enum instances from string values"""
        # Act
        email_type = NotificationTypes("emailNotification")
        wpx_type = NotificationTypes("wpxComment")
        lifecycle_type = NotificationTypes("agentLifecycle")

        # Assert
        assert email_type == NotificationTypes.EMAIL_NOTIFICATION
        assert wpx_type == NotificationTypes.WPX_COMMENT
        assert lifecycle_type == NotificationTypes.AGENT_LIFECYCLE

    def test_enum_invalid_value_raises_error(self):
        """Test that creating enum with invalid value raises ValueError"""
        # Act & Assert
        with pytest.raises(ValueError):
            NotificationTypes("invalidType")

        with pytest.raises(ValueError):
            NotificationTypes("unknown")

        with pytest.raises(ValueError):
            NotificationTypes("")

    def test_enum_case_sensitivity(self):
        """Test that enum values are case sensitive"""
        # Act & Assert
        with pytest.raises(ValueError):
            NotificationTypes("EmailNotification")  # Wrong case

        with pytest.raises(ValueError):
            NotificationTypes("EMAILNOTIFICATION")  # All caps

        with pytest.raises(ValueError):
            NotificationTypes("emailnotification")  # All lowercase

        with pytest.raises(ValueError):
            NotificationTypes("WpxComment")  # Wrong case

        with pytest.raises(ValueError):
            NotificationTypes("AgentLifecycle")  # Wrong case

    def test_enum_str_representation(self):
        """Test string representation of enum values"""
        # Act & Assert
        assert str(NotificationTypes.EMAIL_NOTIFICATION) == "NotificationTypes.EMAIL_NOTIFICATION"
        assert str(NotificationTypes.WPX_COMMENT) == "NotificationTypes.WPX_COMMENT"
        assert str(NotificationTypes.AGENT_LIFECYCLE) == "NotificationTypes.AGENT_LIFECYCLE"

    def test_enum_repr_representation(self):
        """Test repr representation of enum values"""
        # Act
        email_repr = repr(NotificationTypes.EMAIL_NOTIFICATION)
        wpx_repr = repr(NotificationTypes.WPX_COMMENT)
        lifecycle_repr = repr(NotificationTypes.AGENT_LIFECYCLE)

        # Assert
        assert "EMAIL_NOTIFICATION" in email_repr
        assert "WPX_COMMENT" in wpx_repr
        assert "AGENT_LIFECYCLE" in lifecycle_repr

    def test_enum_equality_with_same_values(self):
        """Test equality between same enum values"""
        # Assert
        assert NotificationTypes.EMAIL_NOTIFICATION == NotificationTypes.EMAIL_NOTIFICATION
        assert NotificationTypes.WPX_COMMENT == NotificationTypes.WPX_COMMENT
        assert NotificationTypes.AGENT_LIFECYCLE == NotificationTypes.AGENT_LIFECYCLE

    def test_enum_inequality_with_different_values(self):
        """Test inequality between different enum values"""
        # Assert
        assert NotificationTypes.EMAIL_NOTIFICATION != NotificationTypes.WPX_COMMENT
        assert NotificationTypes.WPX_COMMENT != NotificationTypes.AGENT_LIFECYCLE
        assert NotificationTypes.AGENT_LIFECYCLE != NotificationTypes.EMAIL_NOTIFICATION

    def test_enum_in_collections(self):
        """Test using enum values in collections"""
        # Arrange
        notification_list = [
            NotificationTypes.EMAIL_NOTIFICATION,
            NotificationTypes.WPX_COMMENT,
            NotificationTypes.AGENT_LIFECYCLE
        ]
        
        notification_set = {
            NotificationTypes.EMAIL_NOTIFICATION,
            NotificationTypes.WPX_COMMENT,
            NotificationTypes.AGENT_LIFECYCLE
        }
        
        notification_dict = {
            NotificationTypes.EMAIL_NOTIFICATION: "handle_email",
            NotificationTypes.WPX_COMMENT: "handle_wpx",
            NotificationTypes.AGENT_LIFECYCLE: "handle_lifecycle"
        }

        # Act & Assert
        assert NotificationTypes.EMAIL_NOTIFICATION in notification_list
        assert NotificationTypes.WPX_COMMENT in notification_set
        assert notification_dict[NotificationTypes.AGENT_LIFECYCLE] == "handle_lifecycle"

    def test_enum_as_dictionary_keys(self):
        """Test using enum values as dictionary keys"""
        # Arrange
        handlers = {
            NotificationTypes.EMAIL_NOTIFICATION: lambda: "email_handler",
            NotificationTypes.WPX_COMMENT: lambda: "wpx_handler",
            NotificationTypes.AGENT_LIFECYCLE: lambda: "lifecycle_handler"
        }

        # Act & Assert
        assert handlers[NotificationTypes.EMAIL_NOTIFICATION]() == "email_handler"
        assert handlers[NotificationTypes.WPX_COMMENT]() == "wpx_handler"
        assert handlers[NotificationTypes.AGENT_LIFECYCLE]() == "lifecycle_handler"

    def test_enum_hash_consistency(self):
        """Test that enum values have consistent hash values"""
        # Act
        email_hash1 = hash(NotificationTypes.EMAIL_NOTIFICATION)
        email_hash2 = hash(NotificationTypes.EMAIL_NOTIFICATION)
        
        wpx_hash = hash(NotificationTypes.WPX_COMMENT)
        lifecycle_hash = hash(NotificationTypes.AGENT_LIFECYCLE)

        # Assert
        assert email_hash1 == email_hash2  # Same enum value should have same hash
        assert email_hash1 != wpx_hash  # Different enum values should have different hashes
        assert wpx_hash != lifecycle_hash

    def test_enum_value_attribute(self):
        """Test accessing the value attribute of enum members"""
        # Act & Assert
        assert NotificationTypes.EMAIL_NOTIFICATION.value == "emailNotification"
        assert NotificationTypes.WPX_COMMENT.value == "wpxComment"
        assert NotificationTypes.AGENT_LIFECYCLE.value == "agentLifecycle"

    def test_enum_name_attribute(self):
        """Test accessing the name attribute of enum members"""
        # Act & Assert
        assert NotificationTypes.EMAIL_NOTIFICATION.name == "EMAIL_NOTIFICATION"
        assert NotificationTypes.WPX_COMMENT.name == "WPX_COMMENT"
        assert NotificationTypes.AGENT_LIFECYCLE.name == "AGENT_LIFECYCLE"

    def test_enum_comparison_with_none(self):
        """Test enum comparison with None values"""
        # Act & Assert
        assert NotificationTypes.EMAIL_NOTIFICATION is not None
        assert NotificationTypes.EMAIL_NOTIFICATION != None
        assert not (NotificationTypes.EMAIL_NOTIFICATION == None)