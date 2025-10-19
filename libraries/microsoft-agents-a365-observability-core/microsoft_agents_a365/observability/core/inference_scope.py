# Copyright (c) Microsoft. All rights reserved.

from .agent_details import AgentDetails
from .constants import (
    GEN_AI_PROVIDER_NAME_KEY,
    GEN_AI_REQUEST_CONTENT_KEY,
    GEN_AI_REQUEST_MODEL_KEY,
    GEN_AI_RESPONSE_FINISH_REASONS_KEY,
    GEN_AI_RESPONSE_ID_KEY,
    GEN_AI_USAGE_INPUT_TOKENS_KEY,
    GEN_AI_USAGE_OUTPUT_TOKENS_KEY,
)
from .inference_call_details import InferenceCallDetails
from .opentelemetry_scope import OpenTelemetryScope
from .request import Request
from .tenant_details import TenantDetails


class InferenceScope(OpenTelemetryScope):
    """Provides OpenTelemetry tracing scope for inference call."""

    @staticmethod
    def start(
        details: InferenceCallDetails,
        agent_details: AgentDetails,
        tenant_details: TenantDetails,
        request: Request | None = None,
    ) -> "InferenceScope":
        """Create and start a new scope for inference call.

        Args:
            details: The details of the inference call
            agent_details: The details of the agent making the call
            tenant_details: The details of the tenant
            request: Optional request details for additional context

        Returns:
            A new InferenceScope instance
        """
        return InferenceScope(details, agent_details, tenant_details, request)

    def __init__(
        self,
        inference_call_details: InferenceCallDetails,
        agent_details: AgentDetails,
        tenant_details: TenantDetails,
        request: Request | None = None,
    ):
        """Initialize the agent invocation scope.

        Args:
            inference_call_details: The details of the inference call
            agent_details: The details of the agent making the call
            tenant_details: The details of the tenant
            request: Optional request details for additional context
        """

        super().__init__(
            kind="Client",
            operation_name=inference_call_details.operationName.value,
            activity_name=f"{inference_call_details.operationName.value} {inference_call_details.model}",
            agent_details=agent_details,
            tenant_details=tenant_details,
        )

        # Set request content if provided
        if request:
            self.set_tag_maybe(GEN_AI_REQUEST_CONTENT_KEY, request.content)

        self.set_tag_maybe(GEN_AI_REQUEST_MODEL_KEY, inference_call_details.model)
        self.set_tag_maybe(GEN_AI_PROVIDER_NAME_KEY, inference_call_details.providerName)
        self.set_tag_maybe(GEN_AI_USAGE_INPUT_TOKENS_KEY, inference_call_details.inputTokens)
        self.set_tag_maybe(GEN_AI_USAGE_OUTPUT_TOKENS_KEY, inference_call_details.outputTokens)
        self.set_tag_maybe(
            GEN_AI_RESPONSE_FINISH_REASONS_KEY,
            ",".join(inference_call_details.finishReasons)
            if inference_call_details.finishReasons
            else None,
        )
        self.set_tag_maybe(GEN_AI_RESPONSE_ID_KEY, inference_call_details.responseId)
