# Copyright (c) Microsoft. All rights reserved.

"""
Wraps the OpenAI Agents SDK tracer to integrate with our Kairo Telemetry Solution.
"""

from .trace_instrumentor import KairoInstrumentorOpenAIAgents

__all__ = ["KairoInstrumentorOpenAIAgents"]
