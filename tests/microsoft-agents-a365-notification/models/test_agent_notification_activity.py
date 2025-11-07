# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for AgentNotificationActivity class - Clean Version
"""

from unittest.mock import Mock

import pytest
from microsoft_agents.activity import Activity
from microsoft_agents_a365.notifications.models.agent_notification_activity import (
    AgentNotificationActivity,
)
from microsoft_agents_a365.notifications.models.email_reference import EmailReference
from microsoft_agents_a365.notifications.models.wpx_comment import WpxComment


class TestAgentNotificationActivity:
    """Test cases for AgentNotificationActivity class"""

    def _create_mock_activity(
        self, entities=None, name="agentLifecycle", channel_id=None, value=None, type="message"
    ):
        """Helper to create properly configured mock activity"""
        mock_activity = Mock(spec=Activity)
        # Directly set attributes to ensure they're accessible
        mock_activity.entities = entities
        mock_activity.name = name
        mock_activity.channel_id = channel_id
        mock_activity.value = value
        mock_activity.type = type
        return mock_activity

    def test_init_with_none_activity_raises_error(self):
        """Test that initializing with None activity raises ValueError"""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="activity parameter is required and cannot be None"):
            AgentNotificationActivity(None)

    def test_init_with_valid_activity_no_entities(self):
        """Test initialization with valid activity but no entities"""
        # Arrange
        mock_activity = self._create_mock_activity(entities=None)

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana.activity == mock_activity
        assert ana._email is None
        assert ana._wpx_comment is None
        assert ana.email is None
        assert ana.wpx_comment is None

    def test_init_with_empty_entities_list(self):
        """Test initialization with empty entities list"""
        # Arrange
        mock_activity = self._create_mock_activity(entities=[])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana.activity == mock_activity
        assert ana._email is None
        assert ana._wpx_comment is None

    def test_init_with_email_notification_entity(self):
        """Test initialization with email notification entity"""
        # Arrange
        mock_email_entity = Mock()
        mock_email_entity.type = "EMAILNOTIFICATION"
        mock_email_entity.properties = {"type": "emailNotification"}

        mock_activity = self._create_mock_activity(entities=[mock_email_entity])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana.activity == mock_activity
        assert ana._email is not None
        assert ana._wpx_comment is None

    def test_init_with_wpx_comment_entity(self):
        """Test initialization with WPX comment entity"""
        # Arrange
        mock_wpx_entity = Mock()
        mock_wpx_entity.type = "WPXCOMMENT"
        mock_wpx_entity.properties = {"type": "wpxComment"}

        mock_activity = self._create_mock_activity(entities=[mock_wpx_entity])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana.activity == mock_activity
        assert ana._email is None
        assert ana._wpx_comment is not None

    def test_init_with_multiple_entities(self):
        """Test initialization with multiple entities"""
        # Arrange
        mock_email_entity = Mock()
        mock_email_entity.type = "EMAILNOTIFICATION"
        mock_email_entity.properties = {"type": "emailNotification"}

        mock_wpx_entity = Mock()
        mock_wpx_entity.type = "WPXCOMMENT"
        mock_wpx_entity.properties = {"type": "wpxComment"}

        mock_activity = self._create_mock_activity(entities=[mock_email_entity, mock_wpx_entity])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana.activity == mock_activity
        assert ana._email is not None
        assert ana._wpx_comment is not None

    def test_init_with_invalid_entity_type(self):
        """Test initialization with invalid entity type"""
        # Arrange
        mock_unknown_entity = Mock()
        mock_unknown_entity.type = "UNKNOWN"
        mock_unknown_entity.properties = {"type": "unknown"}

        mock_activity = self._create_mock_activity(entities=[mock_unknown_entity])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana.activity == mock_activity
        assert ana._email is None
        assert ana._wpx_comment is None

    def test_channel_property_with_channel_id(self):
        """Test channel property when activity has channel_id"""
        # Arrange
        mock_channel_id = Mock()
        expected_channel = Mock()
        mock_channel_id.channel = expected_channel
        mock_activity = self._create_mock_activity(entities=None, channel_id=mock_channel_id)

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.channel

        # Assert
        assert result == expected_channel

    def test_channel_property_with_none_channel_id(self):
        """Test channel property when activity has None channel_id"""
        # Arrange
        mock_activity = self._create_mock_activity(entities=None, channel_id=None)

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.channel

        # Assert
        assert result is None

    def test_sub_channel_property_with_channel_id(self):
        """Test sub_channel property when activity has channel_id"""
        # Arrange
        mock_channel_id = Mock()
        mock_channel_id.sub_channel = "testSubChannel"

        mock_activity = self._create_mock_activity(entities=None, channel_id=mock_channel_id)

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.sub_channel

        # Assert
        assert result == "testSubChannel"

    def test_sub_channel_property_with_none_channel_id(self):
        """Test sub_channel property when activity has None channel_id"""
        # Arrange
        mock_activity = self._create_mock_activity(entities=None, channel_id=None)

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.sub_channel

        # Assert
        assert result is None

    def test_value_property(self):
        """Test value property returns activity value"""
        # Arrange
        test_value = {"test": "data"}
        mock_activity = self._create_mock_activity(entities=None, value=test_value)

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.value

        # Assert
        assert result == test_value

    def test_type_property(self):
        """Test type property returns activity type"""
        # Arrange
        test_type = "testMessage"
        mock_activity = self._create_mock_activity(entities=None, type=test_type)

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.type

        # Assert
        assert result == test_type

    def test_email_property_returns_parsed_email(self):
        """Test email property returns parsed EmailReference"""
        # Arrange
        mock_email_entity = Mock()
        mock_email_entity.type = "EMAILNOTIFICATION"
        mock_email_entity.properties = {"type": "emailNotification", "id": "test-email-id"}

        mock_activity = self._create_mock_activity(entities=[mock_email_entity])

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.email

        # Assert
        assert result is not None
        assert isinstance(result, EmailReference)

    def test_wpx_comment_property_returns_parsed_comment(self):
        """Test wpx_comment property returns parsed WpxComment"""
        # Arrange
        mock_wpx_entity = Mock()
        mock_wpx_entity.type = "WPXCOMMENT"
        mock_wpx_entity.properties = {"type": "wpxComment", "odataId": "test-comment-id"}

        mock_activity = self._create_mock_activity(entities=[mock_wpx_entity])

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.wpx_comment

        # Assert
        assert result is not None
        assert isinstance(result, WpxComment)

    def test_as_model_with_valid_data(self):
        """Test as_model method with valid data"""
        # Arrange
        test_value = {"field": "value"}
        mock_activity = self._create_mock_activity(entities=None, value=test_value)

        # Mock model class
        mock_model_class = Mock()
        mock_model_instance = Mock()
        mock_model_class.model_validate.return_value = mock_model_instance

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.as_model(mock_model_class)

        # Assert
        mock_model_class.model_validate.assert_called_once_with(test_value)
        assert result == mock_model_instance

    def test_as_model_with_validation_error(self):
        """Test as_model method when validation fails"""
        # Arrange
        test_value = {"invalid": "data"}
        mock_activity = self._create_mock_activity(entities=None, value=test_value)

        mock_model_class = Mock()
        mock_model_class.model_validate.side_effect = Exception("Validation failed")

        ana = AgentNotificationActivity(mock_activity)

        # Act
        result = ana.as_model(mock_model_class)

        # Assert
        assert result is None

    def test_entity_parsing_with_case_insensitive_type(self):
        """Test entity parsing works with case insensitive type"""
        # Arrange
        mock_email_entity = Mock()
        mock_email_entity.type = "emailnotification"  # lowercase
        mock_email_entity.properties = {"type": "emailNotification"}

        mock_activity = self._create_mock_activity(entities=[mock_email_entity])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana._email is not None

    def test_duplicate_entity_type_handling(self):
        """Test that only first entity of each type is used"""
        # Arrange
        mock_email_entity1 = Mock()
        mock_email_entity1.type = "EMAILNOTIFICATION"
        mock_email_entity1.properties = {"type": "emailNotification", "id": "first"}

        mock_email_entity2 = Mock()
        mock_email_entity2.type = "EMAILNOTIFICATION"
        mock_email_entity2.properties = {"type": "emailNotification", "id": "second"}

        mock_activity = self._create_mock_activity(
            entities=[mock_email_entity1, mock_email_entity2]
        )

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana._email is not None
        # Should use first entity
        assert ana.email.id == "first"

    def test_entity_parsing_with_properties_attribute(self):
        """Test entity parsing using properties attribute"""
        # Arrange
        mock_entity = Mock()
        mock_entity.type = "EMAILNOTIFICATION"
        mock_entity.properties = {"type": "emailNotification", "id": "properties-test"}

        mock_activity = self._create_mock_activity(entities=[mock_entity])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana._email is not None
        assert ana.email.id == "properties-test"

    def test_entity_parsing_only_first_entity_of_each_type(self):
        """Test that only the first entity of each type is parsed"""
        # Arrange
        email_entity1 = Mock()
        email_entity1.type = "EMAILNOTIFICATION"
        email_entity1.properties = {"type": "emailNotification", "id": "email1"}

        email_entity2 = Mock()
        email_entity2.type = "EMAILNOTIFICATION"
        email_entity2.properties = {"type": "emailNotification", "id": "email2"}

        mock_activity = self._create_mock_activity(entities=[email_entity1, email_entity2])

        # Act
        ana = AgentNotificationActivity(mock_activity)

        # Assert
        assert ana._email is not None
        assert ana.email.id == "email1"  # Should be first entity

    def test_as_model_with_none_value(self):
        """Test as_model method with None value"""
        # Arrange
        mock_activity = self._create_mock_activity(entities=None, value=None)

        mock_model_class = Mock()

        ana = AgentNotificationActivity(mock_activity)

        # Act
        ana.as_model(mock_model_class)

        # Assert
        mock_model_class.model_validate.assert_called_once_with({})
