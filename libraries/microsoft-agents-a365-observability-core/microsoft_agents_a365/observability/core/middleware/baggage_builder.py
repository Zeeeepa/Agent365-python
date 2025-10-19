# Copyright (c) Microsoft. All rights reserved.

# Per request baggage builder for OpenTelemetry context propagation.

from typing import Any

from opentelemetry import baggage, context

from ..constants import (
    CORRELATION_ID_KEY,
    GEN_AI_AGENT_AUID_KEY,
    GEN_AI_AGENT_BLUEPRINT_ID_KEY,
    GEN_AI_AGENT_ID_KEY,
    GEN_AI_AGENT_UPN_KEY,
    GEN_AI_CALLER_ID_KEY,
    HIRING_MANAGER_ID_KEY,
    OPERATION_SOURCE_KEY,
    TENANT_ID_KEY,
)


class BaggageBuilder:
    """Per request baggage builder.

    This class provides a fluent API for setting baggage values that will be
    propagated in the OpenTelemetry context.

    Example:
        >>> with BaggageBuilder() \
        ...     .tenant_id("tenant-123") \
        ...     .agent_id("agent-456") \
        ...     .correlation_id("corr-789") \
        ...     .build():
        ...     # Baggage is set in this context
        ...     pass
        >>> # Baggage is restored after exiting the context
    """

    def __init__(self):
        """Initialize the baggage builder."""
        self._pairs: dict[str, str] = {}

    def operation_source(self, value: str | None) -> "BaggageBuilder":
        """Set the operation source baggage value.

        Args:
            value: The operation source value

        Returns:
            Self for method chaining
        """
        self._set(OPERATION_SOURCE_KEY, value)
        return self

    def tenant_id(self, value: str | None) -> "BaggageBuilder":
        """Set the tenant ID baggage value.

        Args:
            value: The tenant ID

        Returns:
            Self for method chaining
        """
        self._set(TENANT_ID_KEY, value)
        return self

    def agent_id(self, value: str | None) -> "BaggageBuilder":
        """Set the agent ID baggage value.

        Args:
            value: The agent ID

        Returns:
            Self for method chaining
        """
        self._set(GEN_AI_AGENT_ID_KEY, value)
        return self

    def agent_auid(self, value: str | None) -> "BaggageBuilder":
        """Set the agent AUID baggage value.

        Args:
            value: The agent AUID

        Returns:
            Self for method chaining
        """
        self._set(GEN_AI_AGENT_AUID_KEY, value)
        return self

    def agent_upn(self, value: str | None) -> "BaggageBuilder":
        """Set the agent UPN baggage value.

        Args:
            value: The agent UPN

        Returns:
            Self for method chaining
        """
        self._set(GEN_AI_AGENT_UPN_KEY, value)
        return self

    def agent_blueprint_id(self, value: str | None) -> "BaggageBuilder":
        """Set the agent blueprint ID baggage value.

        Args:
            value: The agent blueprint ID

        Returns:
            Self for method chaining
        """
        self._set(GEN_AI_AGENT_BLUEPRINT_ID_KEY, value)
        return self

    def correlation_id(self, value: str | None) -> "BaggageBuilder":
        """Set the correlation ID baggage value.

        Args:
            value: The correlation ID

        Returns:
            Self for method chaining
        """
        self._set(CORRELATION_ID_KEY, value)
        return self

    def caller_id(self, value: str | None) -> "BaggageBuilder":
        """Set the caller ID baggage value.

        Args:
            value: The caller ID

        Returns:
            Self for method chaining
        """
        self._set(GEN_AI_CALLER_ID_KEY, value)
        return self

    def hiring_manager_id(self, value: str | None) -> "BaggageBuilder":
        """Set the hiring manager ID baggage value.

        Args:
            value: The hiring manager ID

        Returns:
            Self for method chaining
        """
        self._set(HIRING_MANAGER_ID_KEY, value)
        return self

    def build(self) -> "BaggageScope":
        """Apply the collected baggage to the current context.

        Returns:
            A context manager that restores the previous baggage on exit
        """
        return BaggageScope(self._pairs)

    def _set(self, key: str, value: str | None) -> None:
        """Add a baggage key/value if the value is not None or whitespace.

        Args:
            key: The baggage key
            value: The baggage value
        """
        if value is not None and value.strip():
            self._pairs[key] = value

    @staticmethod
    def set_request_context(
        tenant_id: str | None = None,
        agent_id: str | None = None,
        correlation_id: str | None = None,
    ) -> "BaggageScope":
        """Convenience method to begin a request baggage scope with common fields.

        Args:
            tenant_id: The tenant ID
            agent_id: The agent ID
            correlation_id: The correlation ID

        Returns:
            A context manager that restores the previous baggage on exit
        """
        return (
            BaggageBuilder()
            .tenant_id(tenant_id)
            .agent_id(agent_id)
            .correlation_id(correlation_id)
            .build()
        )


class BaggageScope:
    """Context manager for baggage scope.

    This class manages the lifecycle of baggage values, setting them on enter
    and restoring the previous context on exit.
    """

    def __init__(self, pairs: dict[str, str]):
        """Initialize the baggage scope.

        Args:
            pairs: Dictionary of baggage key-value pairs to set
        """
        self._pairs = pairs
        self._previous_context: Any = None
        self._token: Any = None

    def __enter__(self) -> "BaggageScope":
        """Enter the context and set baggage values.

        Returns:
            Self
        """
        # Get the current context
        self._previous_context = context.get_current()

        # Set all baggage values in the new context
        new_context = self._previous_context
        for key, value in self._pairs.items():
            if value and value.strip():
                new_context = baggage.set_baggage(key, value, context=new_context)

        # Attach the new context
        self._token = context.attach(new_context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and restore previous baggage.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        # Detach and restore previous context
        if self._token is not None:
            context.detach(self._token)
