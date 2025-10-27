# Copyright (c) Microsoft. All rights reserved.

# Execute tool scope for tracing tool execution.

from .agent_details import AgentDetails
from .constants import (
    EXECUTE_TOOL_OPERATION_NAME,
    GEN_AI_TOOL_CALL_ID_KEY,
    GEN_AI_TOOL_DESCRIPTION_KEY,
    GEN_AI_TOOL_NAME_KEY,
    GEN_AI_TOOL_TYPE_KEY,
    SERVER_ADDRESS_KEY,
    SERVER_PORT_KEY,
)
from .opentelemetry_scope import OpenTelemetryScope
from .tenant_details import TenantDetails
from .tool_call_details import ToolCallDetails


class ExecuteToolScope(OpenTelemetryScope):
    """Provides OpenTelemetry tracing scope for AI tool execution operations."""

    @staticmethod
    def start(
        details: ToolCallDetails,
        agent_details: AgentDetails,
        tenant_details: TenantDetails,
    ) -> "ExecuteToolScope":
        """Create and start a new scope for tool execution tracing.

        Args:
            details: The details of the tool call
            agent_details: The details of the agent making the call
            tenant_details: The details of the tenant

        Returns:
            A new ExecuteToolScope instance
        """
        return ExecuteToolScope(details, agent_details, tenant_details)

    def __init__(
        self,
        details: ToolCallDetails,
        agent_details: AgentDetails,
        tenant_details: TenantDetails,
    ):
        """Initialize the tool execution scope.

        Args:
            details: The details of the tool call
            agent_details: The details of the agent making the call
            tenant_details: The details of the tenant
        """
        super().__init__(
            kind="Internal",
            operation_name=EXECUTE_TOOL_OPERATION_NAME,
            activity_name=f"execute_tool {details.tool_name}",
            agent_details=agent_details,
            tenant_details=tenant_details,
        )

        self.set_tag_maybe(GEN_AI_TOOL_NAME_KEY, details.tool_name)
        self.set_tag_maybe("gen_ai.tool.arguments", details.arguments)
        self.set_tag_maybe(GEN_AI_TOOL_TYPE_KEY, details.tool_type)
        self.set_tag_maybe(GEN_AI_TOOL_CALL_ID_KEY, details.tool_call_id)
        self.set_tag_maybe(GEN_AI_TOOL_DESCRIPTION_KEY, details.description)

        if details.endpoint:
            self.set_tag_maybe(SERVER_ADDRESS_KEY, details.endpoint.hostname)
            if details.endpoint.port and details.endpoint.port != 443:
                self.set_tag_maybe(SERVER_PORT_KEY, details.endpoint.port)
