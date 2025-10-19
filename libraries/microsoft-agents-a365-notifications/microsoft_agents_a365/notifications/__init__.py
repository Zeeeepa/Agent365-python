# Copyright (c) Microsoft. All rights reserved.

"""
Microsoft Agents A365 Notifications

Notification and messaging extensions for AI agent applications.
This module provides utilities for handling agent notifications and routing.
"""

from .agents_sdk_extensions import (
    AddRoute,
    AgentApplication,
    AgentNotificationExtensions,
    AgentsSdkExtension,
    ChannelId,
    IActivity,
    IRecipient,
    ITurnContext,
    OnAgentNotification,
    RouteHandler,
    RouteSelector,
)

__all__ = [
    "AddRoute",
    "AgentApplication",
    "AgentNotificationExtensions",
    "AgentsSdkExtension",
    "ChannelId",
    "IActivity",
    "IRecipient",
    "ITurnContext",
    "OnAgentNotification",
    "RouteHandler",
    "RouteSelector",
]
