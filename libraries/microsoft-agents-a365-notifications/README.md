# Microsoft Agent 365 Notifications

This package provides notification and messaging extensions for AI agent applications.

## Features

- **Agent SDK Extensions**: Enhanced notification capabilities for AI agents
- **Channel Management**: Support for different communication channels
- **Activity Handling**: Interfaces for managing agent activities and recipients
- **Role-based Messaging**: Support for role-based communication patterns

## Quick Start

### Import the notification extensions
```python
from microsoft_kairo.notification import agents_sdk_extensions
```

### Basic Usage

The package provides interfaces and utilities for:
- Managing communication channels (`ChannelId`)
- Defining recipients with roles (`IRecipient`)
- Handling agent activities (`IActivity`)
- Assertion helpers for validation

## Installation

```bash
pip install microsoft-agents-a365-notifications
```

## Requirements

- Python 3.9+
- Compatible with AI agent frameworks