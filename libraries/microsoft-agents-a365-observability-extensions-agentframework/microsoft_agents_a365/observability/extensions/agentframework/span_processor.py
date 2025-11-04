# Copyright (c) Microsoft. All rights reserved.

# Custom Span Processor

from opentelemetry.sdk.trace.export import SpanProcessor

from microsoft_agents_a365.observability.core.constants import GEN_AI_OPERATION_NAME_KEY
from microsoft_agents_a365.observability.core.inference_operation_type import InferenceOperationType
from microsoft_agents_a365.observability.core.wrappers.utils import extract_model_name


class AgentFrameworkSpanProcessor(SpanProcessor):
    """
    SpanProcessor for Agent Framework.
    """

    def __init__(self, service_name: str | None = None):
        self.service_name = service_name

    def on_start(self, span, parent_context):
        pass

    def on_end(self, span, parent_context):
            EXECUTE_TOOL_OPERATION = "execute_tool"
            TOOL_CALL_RESULT_TAG = "gen_ai.tool.call.result"
            EVENT_CONTENT_TAG = "gen_ai.event.content"
            if hasattr(span, "attributes"):
                operation_name = span.attributes.get(GEN_AI_OPERATION_NAME_KEY)
                if isinstance(operation_name, str) and operation_name == EXECUTE_TOOL_OPERATION:
                    tool_call_result = span.attributes.get(TOOL_CALL_RESULT_TAG)
                    if tool_call_result is not None:
                        span.set_attribute(EVENT_CONTENT_TAG, tool_call_result)

            

            