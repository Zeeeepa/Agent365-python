# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for EmailReference class
"""

from microsoft_agents_a365.notifications.models.email_reference import EmailReference
from microsoft_agents_a365.notifications.models.notification_types import NotificationTypes


class TestEmailReference:
    """Test cases for EmailReference class"""

    def test_init_with_defaults(self):
        """Test EmailReference initialization with default values"""
        # Arrange & Act
        email_ref = EmailReference()

        # Assert
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION
        assert email_ref.id is None
        assert email_ref.conversation_id is None
        assert email_ref.html_body is None

    def test_init_with_all_values(self):
        """Test EmailReference initialization with all values provided"""
        # Arrange & Act
        email_ref = EmailReference(
            id="email-123", conversation_id="conv-456", html_body="<p>Test email content</p>"
        )

        # Assert
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION
        assert email_ref.id == "email-123"
        assert email_ref.conversation_id == "conv-456"
        assert email_ref.html_body == "<p>Test email content</p>"

    def test_init_with_partial_values(self):
        """Test EmailReference initialization with only some values"""
        # Arrange & Act
        email_ref = EmailReference(id="email-789", conversation_id="conv-101112")

        # Assert
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION
        assert email_ref.id == "email-789"
        assert email_ref.conversation_id == "conv-101112"
        assert email_ref.html_body is None

    def test_type_is_literal_constant(self):
        """Test that type field is always the correct literal value"""
        # Arrange & Act
        email_ref = EmailReference()

        # Assert
        assert email_ref.type == "emailNotification"
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_model_validate_from_dict_with_all_fields(self):
        """Test creating EmailReference from dictionary with all fields"""
        # Arrange
        data = {
            "id": "test-email-id",
            "conversation_id": "test-conv-id",
            "html_body": "<html><body>Test content</body></html>",
        }

        # Act
        email_ref = EmailReference.model_validate(data)

        # Assert
        assert email_ref.id == "test-email-id"
        assert email_ref.conversation_id == "test-conv-id"
        assert email_ref.html_body == "<html><body>Test content</body></html>"
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_model_validate_from_dict_with_partial_fields(self):
        """Test creating EmailReference from dictionary with partial fields"""
        # Arrange
        data = {"id": "partial-email-id"}

        # Act
        email_ref = EmailReference.model_validate(data)

        # Assert
        assert email_ref.id == "partial-email-id"
        assert email_ref.conversation_id is None
        assert email_ref.html_body is None
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_model_validate_from_empty_dict(self):
        """Test creating EmailReference from empty dictionary"""
        # Arrange
        data = {}

        # Act
        email_ref = EmailReference.model_validate(data)

        # Assert
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION
        assert email_ref.id is None
        assert email_ref.conversation_id is None
        assert email_ref.html_body is None

    def test_model_validate_with_extra_fields(self):
        """Test that extra fields are handled appropriately during validation"""
        # Arrange
        data = {
            "id": "test-id",
            "conversation_id": "test-conv",
            "extra_field": "should_be_ignored_or_handled",
            "another_extra": 123,
        }

        # Act
        email_ref = EmailReference.model_validate(data)

        # Assert
        assert email_ref.id == "test-id"
        assert email_ref.conversation_id == "test-conv"
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION
        # Extra fields should not cause errors

    def test_model_validate_with_none_values(self):
        """Test model validation with explicit None values"""
        # Arrange
        data = {"id": None, "conversation_id": None, "html_body": None}

        # Act
        email_ref = EmailReference.model_validate(data)

        # Assert
        assert email_ref.id is None
        assert email_ref.conversation_id is None
        assert email_ref.html_body is None
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_properties_are_accessible(self):
        """Test that all properties are properly accessible"""
        # Arrange
        email_ref = EmailReference(
            id="prop-test-id",
            conversation_id="prop-test-conv",
            html_body="<div>Property test content</div>",
        )

        # Act & Assert
        assert hasattr(email_ref, "id")
        assert hasattr(email_ref, "conversation_id")
        assert hasattr(email_ref, "html_body")
        assert hasattr(email_ref, "type")

        assert email_ref.id == "prop-test-id"
        assert email_ref.conversation_id == "prop-test-conv"
        assert email_ref.html_body == "<div>Property test content</div>"
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_html_body_with_complex_html(self):
        """Test html_body property with complex HTML content"""
        # Arrange
        complex_html = """
        <html>
            <head><title>Test Email</title></head>
            <body>
                <div class="container">
                    <p>Hello <strong>World</strong>!</p>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ul>
                </div>
            </body>
        </html>
        """

        # Act
        email_ref = EmailReference(html_body=complex_html)

        # Assert
        assert email_ref.html_body == complex_html
        assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_id_with_various_formats(self):
        """Test id field with various ID formats"""
        # Test different ID formats
        test_ids = [
            "simple-id",
            "email_123456",
            "msg-abcd-efgh-1234",
            "user@domain.com-msg-001",
            "12345",
        ]

        for test_id in test_ids:
            # Act
            email_ref = EmailReference(id=test_id)

            # Assert
            assert email_ref.id == test_id
            assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_conversation_id_formats(self):
        """Test conversation_id with various formats"""
        # Test different conversation ID formats
        test_conv_ids = [
            "conv-123",
            "conversation_abcd1234",
            "thread-xyz-789",
            "19:meeting_abcd@thread.v2",
        ]

        for conv_id in test_conv_ids:
            # Act
            email_ref = EmailReference(conversation_id=conv_id)

            # Assert
            assert email_ref.conversation_id == conv_id
            assert email_ref.type == NotificationTypes.EMAIL_NOTIFICATION

    def test_model_equality_comparison(self):
        """Test equality comparison between EmailReference instances"""
        # Arrange
        email_ref1 = EmailReference(
            id="test-id", conversation_id="test-conv", html_body="<p>Test</p>"
        )

        email_ref2 = EmailReference(
            id="test-id", conversation_id="test-conv", html_body="<p>Test</p>"
        )

        email_ref3 = EmailReference(
            id="different-id", conversation_id="test-conv", html_body="<p>Test</p>"
        )

        # Act & Assert
        assert email_ref1 == email_ref2  # Same values
        assert email_ref1 != email_ref3  # Different values

    def test_model_dict_representation(self):
        """Test dictionary representation of EmailReference"""
        # Arrange
        email_ref = EmailReference(
            id="dict-test-id", conversation_id="dict-test-conv", html_body="<p>Dict test</p>"
        )

        # Act
        email_dict = email_ref.model_dump()

        # Assert
        expected_dict = {
            "type": "emailNotification",
            "id": "dict-test-id",
            "conversation_id": "dict-test-conv",
            "html_body": "<p>Dict test</p>",
        }
        assert email_dict == expected_dict
