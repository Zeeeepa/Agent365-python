# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for WpxComment class
"""

import pytest
from microsoft_agents_a365.notifications.models.wpx_comment import WpxComment
from microsoft_agents_a365.notifications.models.notification_types import NotificationTypes


class TestWpxComment:
    """Test cases for WpxComment class"""

    def test_init_with_defaults(self):
        """Test WpxComment initialization with default values"""
        # Arrange & Act
        wpx_comment = WpxComment()

        # Assert
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT
        assert wpx_comment.odata_id is None
        assert wpx_comment.document_id is None
        assert wpx_comment.parent_comment_id is None
        assert wpx_comment.comment_id is None

    def test_init_with_all_values(self):
        """Test WpxComment initialization with all values provided"""
        # Arrange & Act
        wpx_comment = WpxComment(
            odata_id="odata-123",
            document_id="doc-456",
            parent_comment_id="parent-789",
            comment_id="comment-101112",
        )

        # Assert
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT
        assert wpx_comment.odata_id == "odata-123"
        assert wpx_comment.document_id == "doc-456"
        assert wpx_comment.parent_comment_id == "parent-789"
        assert wpx_comment.comment_id == "comment-101112"

    def test_init_with_partial_values(self):
        """Test WpxComment initialization with only some values"""
        # Arrange & Act
        wpx_comment = WpxComment(document_id="doc-partial", comment_id="comment-partial")

        # Assert
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT
        assert wpx_comment.document_id == "doc-partial"
        assert wpx_comment.comment_id == "comment-partial"
        assert wpx_comment.odata_id is None
        assert wpx_comment.parent_comment_id is None

    def test_type_is_literal_constant(self):
        """Test that type field is always the correct literal value"""
        # Arrange & Act
        wpx_comment = WpxComment()

        # Assert
        assert wpx_comment.type == "wpxComment"
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_model_validate_from_dict_with_all_fields(self):
        """Test creating WpxComment from dictionary with all fields"""
        # Arrange
        data = {
            "odata_id": "test-odata-id",
            "document_id": "test-doc-id",
            "parent_comment_id": "test-parent-id",
            "comment_id": "test-comment-id",
        }

        # Act
        wpx_comment = WpxComment.model_validate(data)

        # Assert
        assert wpx_comment.odata_id == "test-odata-id"
        assert wpx_comment.document_id == "test-doc-id"
        assert wpx_comment.parent_comment_id == "test-parent-id"
        assert wpx_comment.comment_id == "test-comment-id"
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_model_validate_from_dict_with_partial_fields(self):
        """Test creating WpxComment from dictionary with partial fields"""
        # Arrange
        data = {"document_id": "partial-doc-id", "comment_id": "partial-comment-id"}

        # Act
        wpx_comment = WpxComment.model_validate(data)

        # Assert
        assert wpx_comment.document_id == "partial-doc-id"
        assert wpx_comment.comment_id == "partial-comment-id"
        assert wpx_comment.odata_id is None
        assert wpx_comment.parent_comment_id is None
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_model_validate_from_empty_dict(self):
        """Test creating WpxComment from empty dictionary"""
        # Arrange
        data = {}

        # Act
        wpx_comment = WpxComment.model_validate(data)

        # Assert
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT
        assert wpx_comment.odata_id is None
        assert wpx_comment.document_id is None
        assert wpx_comment.parent_comment_id is None
        assert wpx_comment.comment_id is None

    def test_model_validate_with_extra_fields(self):
        """Test that extra fields are handled appropriately during validation"""
        # Arrange
        data = {
            "document_id": "test-doc",
            "comment_id": "test-comment",
            "extra_field": "should_be_ignored_or_handled",
            "another_extra": 456,
        }

        # Act
        wpx_comment = WpxComment.model_validate(data)

        # Assert
        assert wpx_comment.document_id == "test-doc"
        assert wpx_comment.comment_id == "test-comment"
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT
        # Extra fields should not cause errors

    def test_model_validate_with_none_values(self):
        """Test model validation with explicit None values"""
        # Arrange
        data = {
            "odata_id": None,
            "document_id": None,
            "parent_comment_id": None,
            "comment_id": None,
        }

        # Act
        wpx_comment = WpxComment.model_validate(data)

        # Assert
        assert wpx_comment.odata_id is None
        assert wpx_comment.document_id is None
        assert wpx_comment.parent_comment_id is None
        assert wpx_comment.comment_id is None
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_properties_are_accessible(self):
        """Test that all properties are properly accessible"""
        # Arrange
        wpx_comment = WpxComment(
            odata_id="prop-test-odata",
            document_id="prop-test-doc",
            parent_comment_id="prop-test-parent",
            comment_id="prop-test-comment",
        )

        # Act & Assert
        assert hasattr(wpx_comment, "odata_id")
        assert hasattr(wpx_comment, "document_id")
        assert hasattr(wpx_comment, "parent_comment_id")
        assert hasattr(wpx_comment, "comment_id")
        assert hasattr(wpx_comment, "type")

        assert wpx_comment.odata_id == "prop-test-odata"
        assert wpx_comment.document_id == "prop-test-doc"
        assert wpx_comment.parent_comment_id == "prop-test-parent"
        assert wpx_comment.comment_id == "prop-test-comment"
        assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_comment_hierarchy_root_comment(self):
        """Test root comment (no parent) scenario"""
        # Arrange & Act
        root_comment = WpxComment(
            document_id="doc-hierarchy-test", comment_id="root-comment-1", parent_comment_id=None
        )

        # Assert
        assert root_comment.document_id == "doc-hierarchy-test"
        assert root_comment.comment_id == "root-comment-1"
        assert root_comment.parent_comment_id is None
        assert root_comment.type == NotificationTypes.WPX_COMMENT

    def test_comment_hierarchy_reply_comment(self):
        """Test reply comment (has parent) scenario"""
        # Arrange & Act
        reply_comment = WpxComment(
            document_id="doc-hierarchy-test",
            comment_id="reply-comment-1",
            parent_comment_id="root-comment-1",
        )

        # Assert
        assert reply_comment.document_id == "doc-hierarchy-test"
        assert reply_comment.comment_id == "reply-comment-1"
        assert reply_comment.parent_comment_id == "root-comment-1"
        assert reply_comment.type == NotificationTypes.WPX_COMMENT

    def test_odata_id_with_various_formats(self):
        """Test odata_id field with various formats"""
        # Test different OData ID formats
        test_odata_ids = [
            "/files/document.docx",
            "https://graph.microsoft.com/v1.0/drives/abc/items/123",
            "/drives/drive-id/items/item-id",
            "odata-simple-id",
        ]

        for odata_id in test_odata_ids:
            # Act
            wpx_comment = WpxComment(odata_id=odata_id)

            # Assert
            assert wpx_comment.odata_id == odata_id
            assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_document_id_formats(self):
        """Test document_id with various formats"""
        # Test different document ID formats
        test_doc_ids = [
            "doc-123",
            "document_abcd1234",
            "file-xyz-789",
            "01ABCDEF1234567890ABCDEF1234567890",
        ]

        for doc_id in test_doc_ids:
            # Act
            wpx_comment = WpxComment(document_id=doc_id)

            # Assert
            assert wpx_comment.document_id == doc_id
            assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_comment_id_formats(self):
        """Test comment_id with various formats"""
        # Test different comment ID formats
        test_comment_ids = [
            "comment-123",
            "comment_abcd1234",
            "cmt-xyz-789",
            "12345678-1234-1234-1234-123456789012",
        ]

        for comment_id in test_comment_ids:
            # Act
            wpx_comment = WpxComment(comment_id=comment_id)

            # Assert
            assert wpx_comment.comment_id == comment_id
            assert wpx_comment.type == NotificationTypes.WPX_COMMENT

    def test_model_equality_comparison(self):
        """Test equality comparison between WpxComment instances"""
        # Arrange
        wpx_comment1 = WpxComment(
            odata_id="test-odata",
            document_id="test-doc",
            parent_comment_id="test-parent",
            comment_id="test-comment",
        )

        wpx_comment2 = WpxComment(
            odata_id="test-odata",
            document_id="test-doc",
            parent_comment_id="test-parent",
            comment_id="test-comment",
        )

        wpx_comment3 = WpxComment(
            odata_id="different-odata",
            document_id="test-doc",
            parent_comment_id="test-parent",
            comment_id="test-comment",
        )

        # Act & Assert
        assert wpx_comment1 == wpx_comment2  # Same values
        assert wpx_comment1 != wpx_comment3  # Different values

    def test_model_dict_representation(self):
        """Test dictionary representation of WpxComment"""
        # Arrange
        wpx_comment = WpxComment(
            odata_id="dict-test-odata",
            document_id="dict-test-doc",
            parent_comment_id="dict-test-parent",
            comment_id="dict-test-comment",
        )

        # Act
        comment_dict = wpx_comment.model_dump()

        # Assert
        expected_dict = {
            "type": "wpxComment",
            "odata_id": "dict-test-odata",
            "document_id": "dict-test-doc",
            "parent_comment_id": "dict-test-parent",
            "comment_id": "dict-test-comment",
        }
        assert comment_dict == expected_dict

    def test_nested_comment_thread_scenario(self):
        """Test a complete nested comment thread scenario"""
        # Arrange - Create a thread of comments
        root_comment = WpxComment(
            odata_id="/files/shared-doc.docx",
            document_id="shared-doc-123",
            comment_id="root-001",
            parent_comment_id=None,
        )

        reply1 = WpxComment(
            odata_id="/files/shared-doc.docx",
            document_id="shared-doc-123",
            comment_id="reply-001",
            parent_comment_id="root-001",
        )

        reply2 = WpxComment(
            odata_id="/files/shared-doc.docx",
            document_id="shared-doc-123",
            comment_id="reply-002",
            parent_comment_id="reply-001",
        )

        # Assert - Verify hierarchy structure
        assert root_comment.parent_comment_id is None  # Root has no parent
        assert reply1.parent_comment_id == "root-001"  # Reply to root
        assert reply2.parent_comment_id == "reply-001"  # Reply to reply

        # All should be for same document
        assert root_comment.document_id == reply1.document_id == reply2.document_id

        # All should have correct type
        assert root_comment.type == reply1.type == reply2.type == NotificationTypes.WPX_COMMENT
