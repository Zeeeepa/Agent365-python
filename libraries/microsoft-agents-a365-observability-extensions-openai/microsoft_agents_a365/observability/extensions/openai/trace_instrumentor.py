# Copyright (c) Microsoft. All rights reserved.

# Wrapper for OpenAI Agents SDK

import logging
from collections.abc import Collection
from typing import Any, cast

import opentelemetry.trace as optel_trace
from agents import set_trace_processors
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import Tracer

from microsoft_agents_a365.observability.core import get_tracer, get_tracer_provider, is_configured

from .trace_processor import OpenAIAgentsTraceProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_instruments = ("openai-agents >= 0.2.6",)


class KairoInstrumentorOpenAIAgents(BaseInstrumentor):
    """
    Custom Trace Processor for OpenAI Agents SDK using Kairo.
    Forwards OpenAI Agents SDK traces and spans to Kairo's tracing scopes.

    ```
    """

    def __init__(self):
        """Initialize the KairoInstrumentorOpenAIAgents.
        Raises: RuntimeError: If Kairo is not configured.
        """
        # Verify if Kairo is configured
        kairo_status = is_configured()
        if not kairo_status:
            raise RuntimeError(
                "Kairo is not configured yet. Please configure Kairo before initializing this instrumentor."
            )
        super().__init__()

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs: Any) -> None:
        """Instruments the OpenAI Agents SDK with Kairo tracing."""
        tracer_name = kwargs["tracer_name"] if kwargs.get("tracer_name") else None
        tracer_version = kwargs["tracer_version"] if kwargs.get("tracer_version") else None

        # Get the configured Kairo Tracer
        try:
            tracer = get_tracer(tracer_name, tracer_version)
        except Exception:
            # fallback
            tracer = optel_trace.get_tracer(tracer_name, tracer_version)

        # Get the configured Kairo Tracer Provider instance
        try:
            get_tracer_provider()
        except Exception:
            # fallback
            optel_trace.get_tracer_provider()

        kairo_tracer = cast(Tracer, tracer)

        set_trace_processors([OpenAIAgentsTraceProcessor(kairo_tracer)])

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
