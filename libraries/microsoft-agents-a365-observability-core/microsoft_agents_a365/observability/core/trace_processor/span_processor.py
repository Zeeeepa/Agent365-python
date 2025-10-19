"""Copyright (c) Microsoft. All rights reserved.

Span processor for copying OpenTelemetry baggage entries onto spans.

This implementation assumes `opentelemetry.baggage.get_all` is available with the
signature `get_all(context: Context | None) -> Mapping[str, object]`.

For every new span:
  * Retrieve the current (or parent) context
  * Obtain all baggage entries via `baggage.get_all`
  * For each (key, value) pair with a truthy value not already present as a span
    attribute, add it via `span.set_attribute`
  * Never overwrites existing attributes
"""

from opentelemetry import baggage, context
from opentelemetry.sdk.trace import SpanProcessor as BaseSpanProcessor


class SpanProcessor(BaseSpanProcessor):
    """Span processor that propagates every baggage key/value to span attributes."""

    def __init__(self):
        super().__init__()

    def on_start(self, span, parent_context=None):
        ctx = parent_context or context.get_current()
        if ctx is None:
            return super().on_start(span, parent_context)

        try:
            existing = getattr(span, "attributes", {}) or {}
        except Exception:
            existing = {}

        try:
            baggage_map = baggage.get_all(ctx) or {}
        except Exception:
            baggage_map = {}

        try:
            items = baggage_map.items()
        except AttributeError:
            items = []

        for key, value in items:
            if not value:
                continue
            if key in existing:
                continue
            try:
                span.set_attribute(key, value)
            except Exception:
                continue

        return super().on_start(span, parent_context)

    def on_end(self, span):
        super().on_end(span)
