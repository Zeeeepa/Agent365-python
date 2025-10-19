# Copyright (c) Microsoft. All rights reserved.

# Invoke agent scope for tracing agent invocation.

from .constants import (
    GEN_AI_REQUEST_CONTENT_KEY,
    SERVER_ADDRESS_KEY,
    SERVER_PORT_KEY,
    SESSION_ID_KEY,
)
from .invoke_agent_details import InvokeAgentDetails
from .opentelemetry_scope import OpenTelemetryScope
from .request import Request
from .tenant_details import TenantDetails


class InvokeAgentScope(OpenTelemetryScope):
    """Provides OpenTelemetry tracing scope for AI agent invocation operations."""

    OPERATION_NAME = "invoke_agent"

    @staticmethod
    def start(
        invoke_agent_details: InvokeAgentDetails,
        tenant_details: TenantDetails,
        request: Request | None = None,
    ) -> "InvokeAgentScope":
        """Create and start a new scope for agent invocation tracing.

        Args:
            invoke_agent_details: The details of the agent invocation including endpoint,
                                agent information, and session context
            tenant_details: The details of the tenant
            request: Optional request details for additional context

        Returns:
            A new InvokeAgentScope instance
        """
        return InvokeAgentScope(invoke_agent_details, tenant_details, request)

    def __init__(
        self,
        invoke_agent_details: InvokeAgentDetails,
        tenant_details: TenantDetails,
        request: Request | None = None,
    ):
        """Initialize the agent invocation scope.

        Args:
            invoke_agent_details: The details of the agent invocation
            tenant_details: The details of the tenant
            request: Optional request details for additional context
        """
        activity_name = self.OPERATION_NAME
        if invoke_agent_details.details.agent_name:
            activity_name = f"invoke_agent {invoke_agent_details.details.agent_name}"

        super().__init__(
            kind="Client",
            operation_name=self.OPERATION_NAME,
            activity_name=activity_name,
            agent_details=invoke_agent_details.details,
            tenant_details=tenant_details,
        )

        self.set_tag_maybe(SESSION_ID_KEY, invoke_agent_details.session_id)

        # Set server details
        if invoke_agent_details.endpoint:
            self.set_tag_maybe(SERVER_ADDRESS_KEY, invoke_agent_details.endpoint.hostname)

        # Only record port if it is different from 443
        if (
            invoke_agent_details.endpoint
            and invoke_agent_details.endpoint.port
            and invoke_agent_details.endpoint.port != 443
        ):
            self.set_tag_maybe(SERVER_PORT_KEY, invoke_agent_details.endpoint.port)

        # Set request content if provided
        if request:
            self.set_tag_maybe(GEN_AI_REQUEST_CONTENT_KEY, request.content)
