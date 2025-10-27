# Microsoft Agent 365 Notifications
[![PyPI version](https://badge.fury.io/py/microsoft-agents-a365-notifications.svg)](https://badge.fury.io/py/microsoft-agents-a365-notifications)

Notification and messaging extensions for AI agent applications built with the Microsoft Agent 365 SDK. Enable your agents to handle rich notifications from Microsoft 365 applications like Word, Excel, PowerPoint, and Email.

## What is this?

This library is part of the Microsoft Agent 365 SDK for Python - a comprehensive framework for building enterprise-grade conversational AI agents. The notifications package specifically handles incoming notifications from Microsoft 365 applications, allowing your agents to respond to events like document updates, email mentions, and collaborative activities.

## Key Features

✅ **Microsoft 365 Integration** - Handle notifications from Word, Excel, PowerPoint, and Outlook  
✅ **Channel Routing** - Intelligent routing based on source application and context  
✅ **Type Safety** - Built with Pydantic for automatic validation and type checking  
✅ **Flexible Handlers** - Support for wildcard and specific channel notification handlers  
✅ **Enterprise Ready** - Built for production Microsoft 365 environments  
✅ **Async Support** - Full async/await support for high-performance applications  

## Installation

```bash
pip install microsoft-agents-a365-notifications
```

## Quick Start

### Basic Concepts

The Microsoft Agent 365 Notifications package enables your agents to receive and respond to notifications from Microsoft 365 applications. Key concepts include:

- **Notification Handlers**: Functions that process incoming notifications
- **Channel Routing**: Route notifications based on the source application
- **Sub-Channel Filtering**: Handle specific types of notifications (email, documents, etc.)
- **Context Integration**: Access rich context about the notification source

### Getting Started

1. Install the package: `pip install microsoft-agents-a365-notifications`
2. Configure your agent application with notification support
3. Register handlers for specific Microsoft 365 applications
4. Process incoming notifications with full context

## Supported Microsoft 365 Applications

| Application | Sub-Channel ID | Description |
|-------------|----------------|-------------|
| **Email** | `email` | Handle mentions and email-based interactions |
| **Word** | `word` | Respond to document collaboration events |
| **Excel** | `excel` | Process spreadsheet updates and analysis requests |
| **PowerPoint** | `powerpoint` | Handle presentation collaboration notifications |
| **Federated Knowledge** | `federatedknowledgeservice` | Enterprise knowledge base interactions |

## Advanced Usage

### Notification Processing Features

- **Custom Route Priorities**: Configure handler execution order for different notification types
- **Authentication Integration**: Seamless integration with Microsoft 365 authentication flows  
- **Rich Context Access**: Access detailed metadata about notification sources and content
- **Flexible Filtering**: Support for wildcard matching and specific application targeting

### Notification Types

The package supports various notification scenarios:
- Document collaboration events (Word, Excel, PowerPoint)
- Email mentions and interactions  
- Enterprise knowledge base updates
- Custom application notifications

## Architecture

The notifications package follows a clean architecture pattern:

- **Route Selectors**: Determine which notifications match specific handlers
- **Activity Wrappers**: Strongly-typed wrappers around raw notification data  
- **Handler Registry**: Manages registration and execution of notification handlers
- **Channel Filtering**: Intelligent filtering based on Microsoft 365 application context

## Integration with Microsoft Agent 365 SDK

This package works seamlessly with other Microsoft Agent 365 SDK components:

| Package | Integration |
|---------|-------------|
| `microsoft-agents-activity` | Core activity types and protocols |
| `microsoft-agents-hosting-core` | Agent lifecycle and middleware |
| `microsoft-agents-authentication-msal` | Microsoft 365 authentication |
| `microsoft-agents-hosting-teams` | Teams-specific hosting |

## Sample Applications

Check out these working examples:

| Sample | Description | Location |
|--------|-------------|----------|
| **Word Assistant** | Agent that helps with document writing | `samples/word-assistant/` |
| **Excel Analyzer** | Data analysis agent for spreadsheets | `samples/excel-analyzer/` |
| **Email Summarizer** | Automatic email summary agent | `samples/email-summarizer/` |
| **Multi-App Agent** | Handles notifications from all M365 apps | `samples/multi-app-agent/` |

## Requirements

- **Python**: 3.11+
- **Dependencies**: 
  - `typing-extensions >= 4.0.0`
  - `microsoft-agents-activity >= 0.4.0`
  - `microsoft-agents-hosting-core >= 0.4.0`
  - `pydantic >= 2.0.0`

## Common Use Cases

### Document Collaboration
- Respond to document updates and changes
- Provide writing assistance and suggestions
- Generate document summaries and reviews
- Handle collaborative editing scenarios

### Data Analysis Assistant  
- Process spreadsheet updates and changes
- Generate insights from data modifications
- Create visualizations and reports
- Assist with data analysis workflows

### Email Productivity
- Handle email mentions and notifications
- Draft responses and follow-ups
- Extract action items from conversations
- Manage email-based workflows

## Quick Links

📦 [All SDK Packages on PyPI](TODO: Update when packages are published)  
📖 [Complete Documentation](https://github.com/microsoft/Agent365/tree/main/python)  
💡 [Python Samples Repository](https://github.com/microsoft/Agent365/tree/main/samples)  
🐛 [Report Issues](https://github.com/microsoft/Agent365/issues)  
🔧 [Microsoft 365 Developer Center](https://developer.microsoft.com/microsoft-365/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.