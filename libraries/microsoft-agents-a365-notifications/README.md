# microsoft-agents-a365-notifications

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-notifications?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-notifications)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-notifications?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-notifications)

Notification and messaging extensions for AI agent applications. This package provides utilities for handling agent notifications, lifecycle events, and routing across different channels and subchannels in Microsoft 365 applications.

## Installation

```bash
pip install microsoft-agents-a365-notifications
```

## Usage

### Basic Notification Handler

```python
from microsoft_agents_a365.notifications import AgentNotification, AgentNotificationActivity
from microsoft_agents.activity import ChannelId
from microsoft_agents.hosting.core import TurnContext, TurnState

# Initialize notification handler
agent_notification = AgentNotification(
    app=app,
    known_subchannels=["email", "word", "excel"],
)

# Register notification handler for specific channel
@agent_notification.on_agent_notification(
    channel_id=ChannelId(channel="msteams", sub_channel="email")
)
async def handle_email_notification(
    context: TurnContext,
    state: TurnState,
    notification: AgentNotificationActivity
):
    # Process email notification
    print(f"Received notification: {notification.notification_type}")
    await context.send_activity("Processing your email notification")
```

### Handle Multiple Subchannels

```python
# Handle all notifications for a channel (wildcard)
@agent_notification.on_agent_notification(
    channel_id=ChannelId(channel="msteams", sub_channel="*")
)
async def handle_all_notifications(
    context: TurnContext,
    state: TurnState,
    notification: AgentNotificationActivity
):
    # Route based on notification type
    if notification.notification_type == "email":
        await handle_email(context, notification)
    elif notification.notification_type == "document":
        await handle_document(context, notification)
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
