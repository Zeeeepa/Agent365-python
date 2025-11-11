# Copyright (c) Microsoft. All rights reserved.

"""
Wraps the OpenAI Agents SDK tracer to integrate with our Agent365 Telemetry Solution.
"""

from .trace_instrumentor import OpenAIAgentsTraceInstrumentor

__all__ = ["OpenAIAgentsTraceInstrumentor"]
