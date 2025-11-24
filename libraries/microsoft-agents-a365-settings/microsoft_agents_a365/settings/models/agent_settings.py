# Copyright (c) Microsoft. All rights reserved.

"""Model for agent instance settings."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, Field

from .agent_setting_property import AgentSettingProperty


def _utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(UTC)


class AgentSettings(BaseModel):
    """Represents the settings for a specific agent instance."""

    id: str = Field(default="", description="The unique identifier of the settings.")
    agent_instance_id: str = Field(
        default="",
        alias="agentInstanceId",
        description="The agent instance identifier these settings belong to.",
    )
    template_id: Optional[str] = Field(
        default=None,
        alias="templateId",
        description="The template identifier these settings are based on.",
    )
    agent_type: str = Field(default="", alias="agentType", description="The agent type.")
    properties: list[AgentSettingProperty] = Field(
        default_factory=list,
        description="The collection of setting properties and their values.",
    )
    created_at: datetime = Field(
        default_factory=_utc_now,
        alias="createdAt",
        description="The date and time when these settings were created.",
    )
    modified_at: datetime = Field(
        default_factory=_utc_now,
        alias="modifiedAt",
        description="The date and time when these settings were last modified.",
    )

    model_config = {"populate_by_name": True}
