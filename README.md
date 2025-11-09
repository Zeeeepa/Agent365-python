# Microsoft Agents A365 SDK - Python

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-observability-core?label=PyPI&logo=pypi)](https://pypi.org/search/?q=microsoft-agents-a365)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-observability-core?label=Downloads&logo=pypi)](https://pypi.org/search/?q=microsoft-agents-a365)
[![Build Status](https://img.shields.io/github/actions/workflow/status/microsoft/Agent365-python/build.yml?branch=main&label=Build&logo=github)](https://github.com/microsoft/Agent365-python/actions)
[![License](https://img.shields.io/github/license/microsoft/Agent365-python?label=License)](LICENSE.md)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)
[![Contributors](https://img.shields.io/github/contributors/microsoft/Agent365-python?label=Contributors&logo=github)](https://github.com/microsoft/Agent365-python/graphs/contributors)

The Microsoft Agents A365 SDK extends the Microsoft 365 Agents SDK with enterprise-grade capabilities for building sophisticated agents. This SDK provides comprehensive tooling for observability, notifications, runtime utilities, and development tools that help developers create production-ready agents for platforms including M365, Teams, Copilot Studio, and Webchat.

The Microsoft Agents A365 SDK focuses on four core areas:

- **Observability**: Comprehensive tracing, caching, and monitoring capabilities for agent applications
- **Notifications**: Agent notification services and models for handling user notifications
- **Runtime**: Core utilities and extensions for agent runtime operations
- **Tooling**: Developer tools and utilities for building sophisticated agent applications

## Current Project State

This project is currently in active development. Packages are published to PyPI as they become available.

### Public PyPI feed

The best way to consume this SDK is via our PyPI packages found here: [pypi.org](https://pypi.org/search/?q=microsoft-agents-a365). All packages begin with **microsoft-agents-a365**.

## Working with this codebase

### Prerequisites

- Python 3.10 or later
- pip or uv package manager
- Git

### Building the project

1. Clone the repository:

   ```bash
   git clone https://github.com/microsoft/Agent365-python.git
   cd Agent365-python
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Build the packages:

   ```bash
   # Set the version
   export AGENT365_PYTHON_SDK_PACKAGE_VERSION="0.1.0"  # On Windows: $env:AGENT365_PYTHON_SDK_PACKAGE_VERSION = "0.1.0"
   
   # Build all packages
   uv build --all-packages --wheel
   ```

4. Run tests:

   ```bash
   pytest tests/
   ```

For more detailed build instructions, see the [BUILD.md](BUILD.md).

## Project Structure

- **libraries/microsoft-agents-a365-notifications**: Microsoft Agents A365 Notifications - Agent notification services and models
- **libraries/microsoft-agents-a365-observability-core**: Microsoft Agents A365 Observability Core - Core observability functionality
- **libraries/microsoft-agents-a365-observability-extensions-agentframework**: Agent Framework observability extensions
- **libraries/microsoft-agents-a365-observability-extensions-langchain**: LangChain observability extensions
- **libraries/microsoft-agents-a365-observability-extensions-openai**: OpenAI observability extensions
- **libraries/microsoft-agents-a365-observability-extensions-semantickernel**: Semantic Kernel observability extensions
- **libraries/microsoft-agents-a365-runtime**: Microsoft Agents A365 Runtime - Core runtime utilities and extensions
- **libraries/microsoft-agents-a365-tooling**: Microsoft Agents A365 Tooling - Agent tooling and MCP integration
- **libraries/microsoft-agents-a365-tooling-extensions-agentframework**: Agent Framework tooling extensions
- **libraries/microsoft-agents-a365-tooling-extensions-azureaifoundry**: Azure AI Foundry tooling extensions
- **libraries/microsoft-agents-a365-tooling-extensions-openai**: OpenAI tooling extensions
- **libraries/microsoft-agents-a365-tooling-extensions-semantickernel**: Semantic Kernel tooling extensions
- **samples/**: For sample applications, see the [Agent365-Samples Repository](https://github.com/microsoft/Agent365-Samples/tree/main/python)
- **tests/**: Unit and integration tests

## Support

For issues, questions, or feedback:

- **Issues**: Please file issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- **Documentation**: See the [Microsoft Agents A365 Developer Documentation](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/)
- **Security**: For security issues, please see [SECURITY.md](SECURITY.md)

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit <https://cla.opensource.microsoft.com>.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

## Useful Links

### Microsoft 365 Agents SDK

The core SDK for building conversational AI agents for Microsoft 365 platforms.

- [Microsoft 365 Agents SDK](https://aka.ms/agents)
- [Agents-for-net Repository](https://github.com/Microsoft/Agents-for-net)
- [Agents-for-js Repository](https://github.com/Microsoft/Agents-for-js)
- [Agents-for-python Repository](https://github.com/Microsoft/Agents-for-python)
- [Official Agents Documentation](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/)

### Microsoft Agents A365 SDK

Enterprise-grade extensions for observability, notifications, runtime utilities, and developer tools.

- [Agent365-dotnet Repository](https://github.com/microsoft/Agent365-dotnet)
- [Agent365-python Repository](https://github.com/microsoft/Agent365-python) - You are here
- [Agent365-nodejs Repository](https://github.com/microsoft/Agent365-nodejs)
- [Agent365-Samples Repository](https://github.com/microsoft/Agent365-Samples)
- [Microsoft Agents A365 Developer Documentation](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/)

### Additional Resources

- [Python Documentation](https://learn.microsoft.com/en-us/python/api/?view=m365-agents-sdk&preserve-view=true)

## Data Collection Notice

The software may collect information about you and your use of the software and send it to Microsoft. Microsoft may use this information to provide services and improve our products and services. You may turn off the telemetry as described in the repository. There are also some features in the software that may enable you and Microsoft to collect data from users of your applications. If you use these features, you must comply with applicable law, including providing appropriate notices to users of your applications together with a copy of Microsoft's privacy statement. Our privacy statement is located at <https://go.microsoft.com/fwlink/?LinkID=824704>. You can learn more about data collection and use in the help documentation and our privacy statement. Your use of the software operates as your consent to these practices.
