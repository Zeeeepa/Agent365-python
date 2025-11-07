# Copyright (c) Microsoft. All rights reserved.

"""
Unit tests for AgentNotification class
"""

from unittest.mock import AsyncMock, Mock

import pytest
from microsoft_agents.activity import Activity, ChannelId
from microsoft_agents.hosting.core import TurnContext
from microsoft_agents.hosting.core.app.state import TurnState

from microsoft_agents_a365.notifications.agent_notification import AgentNotification
from microsoft_agents_a365.notifications.models.agent_notification_activity import (
    AgentNotificationActivity,
)
from microsoft_agents_a365.notifications.models.agent_subchannel import (
    AgentSubChannel,
)


class TestAgentSubChannel:
    """Test cases for AgentSubChannel enum"""

    def test_subchannel_values(self):
        """Test that AgentSubChannel has correct enum values"""
        # Arrange & Act & Assert
        assert AgentSubChannel.EMAIL == "email"
        assert AgentSubChannel.EXCEL == "excel"
        assert AgentSubChannel.WORD == "word"
        assert AgentSubChannel.POWERPOINT == "powerpoint"
        assert AgentSubChannel.FEDERATED_KNOWLEDGE_SERVICE == "federatedknowledgeservice"

    def test_subchannel_string_inheritance(self):
        """Test that AgentSubChannel inherits from str"""
        # Arrange & Act & Assert
        assert isinstance(AgentSubChannel.EMAIL, str)
        assert isinstance(AgentSubChannel.WORD, str)
        assert isinstance(AgentSubChannel.EXCEL, str)
        assert isinstance(AgentSubChannel.POWERPOINT, str)

    def test_subchannel_comparison(self):
        """Test that subchannels can be compared as strings"""
        # Arrange & Act & Assert
        assert AgentSubChannel.EMAIL == "email"
        assert AgentSubChannel.WORD == "word"
        assert AgentSubChannel.EMAIL != AgentSubChannel.WORD


class TestAgentNotification:
    """Test cases for AgentNotification class"""

    def test_init_with_default_subchannels(self):
        """Test AgentNotification initialization with default subchannels"""
        # Arrange
        mock_app = Mock()

        # Act
        agent_notification = AgentNotification(mock_app)

        # Assert
        assert agent_notification._app == mock_app
        assert len(agent_notification._known_subchannels) == 5
        assert "email" in agent_notification._known_subchannels
        assert "word" in agent_notification._known_subchannels
        assert "excel" in agent_notification._known_subchannels
        assert "powerpoint" in agent_notification._known_subchannels
        assert "federatedknowledgeservice" in agent_notification._known_subchannels

    def test_init_with_custom_subchannels(self):
        """Test AgentNotification initialization with custom subchannels"""
        # Arrange
        mock_app = Mock()
        custom_subchannels = ["email", "word", "custom_channel"]

        # Act
        agent_notification = AgentNotification(mock_app, custom_subchannels)

        # Assert
        assert agent_notification._app == mock_app
        assert len(agent_notification._known_subchannels) == 3
        assert "email" in agent_notification._known_subchannels
        assert "word" in agent_notification._known_subchannels
        assert "custom_channel" in agent_notification._known_subchannels

    def test_init_with_enum_subchannels(self):
        """Test initialization with AgentSubChannel enum values"""
        # Arrange
        mock_app = Mock()
        enum_subchannels = [AgentSubChannel.EMAIL, AgentSubChannel.WORD]

        # Act
        agent_notification = AgentNotification(mock_app, enum_subchannels)

        # Assert
        assert len(agent_notification._known_subchannels) == 2
        assert "email" in agent_notification._known_subchannels
        assert "word" in agent_notification._known_subchannels

    def test_normalize_subchannel_with_string(self):
        """Test _normalize_subchannel with string input"""
        # Arrange & Act & Assert
        assert AgentNotification._normalize_subchannel("EMAIL") == "email"
        assert AgentNotification._normalize_subchannel("  Word  ") == "word"
        assert AgentNotification._normalize_subchannel("custom") == "custom"

    def test_normalize_subchannel_with_enum(self):
        """Test _normalize_subchannel with enum input"""
        # Arrange & Act & Assert
        assert AgentNotification._normalize_subchannel(AgentSubChannel.EMAIL) == "email"
        assert AgentNotification._normalize_subchannel(AgentSubChannel.WORD) == "word"

    def test_normalize_subchannel_with_none(self):
        """Test _normalize_subchannel with None input"""
        # Arrange & Act & Assert
        assert AgentNotification._normalize_subchannel(None) == ""

    def test_on_agent_notification_decorator_creation(self):
        """Test that on_agent_notification creates proper decorator"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)
        channel_id = ChannelId(channel="agents", sub_channel="email")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)

        # Assert
        assert callable(decorator)

    @pytest.mark.asyncio
    async def test_on_agent_notification_route_matching_exact_channel(self):
        """Test route matching with exact channel and subchannel"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Mock activity and context
        mock_activity = Mock()
        mock_activity.channel_id = ChannelId(channel="agents", sub_channel="email")
        mock_context = Mock(spec=TurnContext)
        mock_context.activity = mock_activity

        channel_id = ChannelId(channel="agents", sub_channel="email")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)
        mock_handler = Mock()
        decorator(mock_handler)
        route_selector = mock_app.add_route.call_args[0][0]
        result = route_selector(mock_context)

        # Assert
        mock_app.add_route.assert_called_once()
        assert result is True

    @pytest.mark.asyncio
    async def test_on_agent_notification_route_matching_wildcard_subchannel(self):
        """Test route matching with wildcard subchannel"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Mock activity and context
        mock_activity = Mock()
        mock_activity.channel_id = ChannelId(channel="agents", sub_channel="email")
        mock_context = Mock(spec=TurnContext)
        mock_context.activity = mock_activity

        channel_id = ChannelId(channel="agents", sub_channel="*")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)
        mock_handler = Mock()
        decorator(mock_handler)
        route_selector = mock_app.add_route.call_args[0][0]
        result = route_selector(mock_context)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_on_agent_notification_route_not_matching_different_channel(self):
        """Test route not matching with different channel"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Mock activity and context with different channel
        mock_activity = Mock()
        mock_activity.channel_id = ChannelId(channel="different", sub_channel="email")
        mock_context = Mock(spec=TurnContext)
        mock_context.activity = mock_activity

        channel_id = ChannelId(channel="agents", sub_channel="email")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)
        mock_handler = Mock()
        decorator(mock_handler)
        route_selector = mock_app.add_route.call_args[0][0]
        result = route_selector(mock_context)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_on_agent_notification_handler_execution(self):
        """Test that the handler is properly executed"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        mock_handler = AsyncMock()
        mock_context = Mock(spec=TurnContext)
        mock_state = Mock(spec=TurnState)
        mock_activity = Mock(spec=Activity)
        mock_activity.entities = []  # Add the missing entities attribute
        mock_activity.name = "agentLifecycle"  # Add the missing name attribute
        mock_context.activity = mock_activity

        channel_id = ChannelId(channel="agents", sub_channel="email")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)
        wrapped_handler = decorator(mock_handler)

        # Execute the wrapped handler
        await wrapped_handler(mock_context, mock_state)

        # Assert
        mock_handler.assert_called_once()
        args = mock_handler.call_args[0]
        assert args[0] == mock_context
        assert args[1] == mock_state
        assert isinstance(args[2], AgentNotificationActivity)

    def test_on_email_decorator(self):
        """Test on_email convenience method"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Act
        decorator = agent_notification.on_email()
        mock_handler = Mock()
        decorator(mock_handler)

        # Assert
        assert callable(decorator)
        mock_app.add_route.assert_called_once()

    def test_on_word_decorator(self):
        """Test on_word convenience method"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Act
        decorator = agent_notification.on_word()
        mock_handler = Mock()
        decorator(mock_handler)

        # Assert
        assert callable(decorator)
        mock_app.add_route.assert_called_once()

    def test_on_excel_decorator(self):
        """Test on_excel convenience method"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Act
        decorator = agent_notification.on_excel()
        mock_handler = Mock()
        decorator(mock_handler)

        # Assert
        assert callable(decorator)
        mock_app.add_route.assert_called_once()

    def test_on_powerpoint_decorator(self):
        """Test on_powerpoint convenience method"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        # Act
        decorator = agent_notification.on_powerpoint()
        mock_handler = Mock()
        decorator(mock_handler)

        # Assert
        assert callable(decorator)
        mock_app.add_route.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_selector_with_no_channel_id(self):
        """Test route selector when activity has no channel_id"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        agent_notification = AgentNotification(mock_app)

        mock_activity = Mock()
        mock_activity.channel_id = None
        mock_context = Mock(spec=TurnContext)
        mock_context.activity = mock_activity

        channel_id = ChannelId(channel="agents", sub_channel="email")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)
        mock_handler = Mock()
        decorator(mock_handler)
        route_selector = mock_app.add_route.call_args[0][0]
        result = route_selector(mock_context)

        # Assert
        assert result is False

    def test_init_with_empty_subchannels_list(self):
        """Test initialization with empty subchannels list"""
        # Arrange
        mock_app = Mock()
        empty_subchannels = []

        # Act
        agent_notification = AgentNotification(mock_app, empty_subchannels)

        # Assert
        assert len(agent_notification._known_subchannels) == 0

    def test_init_with_mixed_subchannel_types(self):
        """Test initialization with mixed string and enum subchannels"""
        # Arrange
        mock_app = Mock()
        mixed_subchannels = ["email", AgentSubChannel.WORD, "custom"]

        # Act
        agent_notification = AgentNotification(mock_app, mixed_subchannels)

        # Assert
        assert len(agent_notification._known_subchannels) == 3
        assert "email" in agent_notification._known_subchannels
        assert "word" in agent_notification._known_subchannels
        assert "custom" in agent_notification._known_subchannels

    @pytest.mark.asyncio
    async def test_route_selector_unknown_subchannel(self):
        """Test route selector with unknown subchannel"""
        # Arrange
        mock_app = Mock()
        mock_app.add_route = Mock()
        known_subchannels = ["email", "word"]  # Don't include "excel"
        agent_notification = AgentNotification(mock_app, known_subchannels)

        mock_activity = Mock()
        mock_activity.channel_id = ChannelId(channel="agents", sub_channel="excel")
        mock_context = Mock(spec=TurnContext)
        mock_context.activity = mock_activity

        # Try to register for unknown subchannel
        channel_id = ChannelId(channel="agents", sub_channel="excel")

        # Act
        decorator = agent_notification.on_agent_notification(channel_id)
        mock_handler = Mock()
        decorator(mock_handler)
        route_selector = mock_app.add_route.call_args[0][0]
        result = route_selector(mock_context)

        # Assert
        assert result is False
