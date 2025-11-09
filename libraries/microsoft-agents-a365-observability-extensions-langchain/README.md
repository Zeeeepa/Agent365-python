# microsoft-agents-a365-observability-extensions-langchain

[![PyPI](https://img.shields.io/pypi/v/microsoft-agents-a365-observability-extensions-langchain?label=PyPI&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-langchain)
[![PyPI Downloads](https://img.shields.io/pypi/dm/microsoft-agents-a365-observability-extensions-langchain?label=Downloads&logo=pypi)](https://pypi.org/project/microsoft-agents-a365-observability-extensions-langchain)

Observability extensions for LangChain framework. This package provides OpenTelemetry tracing integration for LangChain-based AI applications with automatic instrumentation for chains, agents, and tools.

## Installation

```bash
pip install microsoft-agents-a365-observability-extensions-langchain
```

## Usage

### Basic Configuration

```python
from microsoft_agents_a365.observability.core import configure
from microsoft_agents_a365.observability.extensions.langchain import (
    CustomLangChainInstrumentor
)

# Configure observability
configure(
    service_name="my-langchain-agent",
    service_namespace="ai.agents"
)

# Enable automatic instrumentation
instrumentor = CustomLangChainInstrumentor()
instrumentor.instrument()

# Your LangChain code is now automatically traced
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# All LangChain operations will be automatically instrumented
chain = LLMChain(llm=llm, prompt=prompt_template)
result = chain.run(input_text)
```

## Support

For issues, questions, or feedback:

- File issues in the [GitHub Issues](https://github.com/microsoft/Agent365-python/issues) section
- See the [main documentation](../../../README.md) for more information

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT License - see the [LICENSE](../../../LICENSE.md) file for details.
