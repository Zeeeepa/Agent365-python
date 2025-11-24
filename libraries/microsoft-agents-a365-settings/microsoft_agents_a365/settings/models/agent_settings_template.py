# Copyright (c) Microsoft. All rights reserved.

"""Model for agent settings template."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .agent_setting_property import AgentSettingProperty


class AgentSettingsTemplate(BaseModel):
    """Represents a settings template for a specific agent type."""

    id: str = Field(default="", description="The unique identifier of the template.")
    agent_type: str = Field(
        default="", alias="agentType", description="The agent type this template applies to."
    )
    name: str = Field(default="", description="The name of the template.")
    description: Optional[str] = Field(default=None, description="The description of the template.")
    version: str = Field(default="1.0", description="The version of the template.")
    properties: list[AgentSettingProperty] = Field(
        default_factory=list,
        description="The collection of setting properties defined in this template.",
    )

    model_config = {"populate_by_name": True}
