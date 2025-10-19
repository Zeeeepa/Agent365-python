from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from enum import Enum
from typing import Any, TypeVar

from microsoft_agents.activity import ChannelId
from microsoft_agents.hosting.core import TurnContext
from microsoft_agents.hosting.core.app.state import TurnState
from .models.agent_notification_activity import AgentNotificationActivity

TContext = TypeVar("TContext", bound=TurnContext)
TState = TypeVar("TState", bound=TurnState)

AgentHandler = Callable[[TContext, TState, AgentNotificationActivity], Awaitable[None]]


class AgentSubChannel(str, Enum):
    EMAIL = "email"
    EXCEL = "excel"
    WORD = "word"
    POWERPOINT = "powerpoint"
    FEDERATED_KNOWLEDGE_SERVICE = "federatedknowledgeservice"


class AgentNotification:
    def __init__(
        self,
        app: Any,
        known_subchannels: Iterable[str | AgentSubChannel] | None = None,
    ):
        self._app = app
        if known_subchannels is None:
            source_subchannels: Iterable[str | AgentSubChannel] = AgentSubChannel
        else:
            source_subchannels = known_subchannels

        self._known_subchannels = {
            normalized
            for normalized in (
                self._normalize_subchannel(sub_channel) for sub_channel in source_subchannels
            )
            if normalized
        }

    def on_agent_notification(
        self,
        channel_id: ChannelId,
        **kwargs: Any,
    ):
        registered_channel = channel_id.channel.lower()
        registered_subchannel = (channel_id.sub_channel or "*").lower()

        def route_selector(context: TurnContext) -> bool:
            ch = context.activity.channel_id
            received_channel = ch.channel if ch else ""
            received_subchannel = ch.sub_channel if ch else ""
            received_channel = received_channel.lower()
            received_subchannel = received_subchannel.lower()
            if received_channel != registered_channel:
                return False
            if registered_subchannel == "*":
                return True
            if registered_subchannel not in self._known_subchannels:
                return False
            return received_subchannel == registered_subchannel

        def create_handler(handler: AgentHandler):
            async def route_handler(context: TurnContext, state: TurnState):
                ana = AgentNotificationActivity(context.activity)
                await handler(context, state, ana)

            return route_handler

        def decorator(handler: AgentHandler):
            route_handler = create_handler(handler)
            self._app.add_route(route_selector, route_handler, **kwargs)
            return route_handler

        return decorator

    def on_email(
        self, **kwargs: Any
    ) -> Callable[[AgentHandler], Callable[[TurnContext, TurnState], Awaitable[None]]]:
        return self.on_agent_notification(
            ChannelId(channel="agents", sub_channel=AgentSubChannel.EMAIL), **kwargs
        )

    def on_word(
        self, **kwargs: Any
    ) -> Callable[[AgentHandler], Callable[[TurnContext, TurnState], Awaitable[None]]]:
        return self.on_agent_notification(
            ChannelId(channel="agents", sub_channel=AgentSubChannel.WORD), **kwargs
        )

    def on_excel(
        self, **kwargs: Any
    ) -> Callable[[AgentHandler], Callable[[TurnContext, TurnState], Awaitable[None]]]:
        return self.on_agent_notification(
            ChannelId(channel="agents", sub_channel=AgentSubChannel.EXCEL), **kwargs
        )

    def on_powerpoint(
        self, **kwargs: Any
    ) -> Callable[[AgentHandler], Callable[[TurnContext, TurnState], Awaitable[None]]]:
        return self.on_agent_notification(
            ChannelId(channel="agents", sub_channel=AgentSubChannel.POWERPOINT), **kwargs
        )

    @staticmethod
    def _normalize_subchannel(value: str | AgentSubChannel | None) -> str:
        if value is None:
            return ""
        resolved = value.value if isinstance(value, AgentSubChannel) else str(value)
        return resolved.lower().strip()
