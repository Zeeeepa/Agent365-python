# Copyright (c) Microsoft. All rights reserved.

# Agent details class.
from dataclasses import dataclass


@dataclass
class AgentDetails:
    """Details about an AI agent."""

    agent_id: str
    conversation_id: str | None = None
    agent_name: str | None = None
    agent_description: str | None = None
    icon_uri: str | None = None
