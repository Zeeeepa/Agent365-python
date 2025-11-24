# Copyright (c) Microsoft. All rights reserved.

"""Model for an individual agent setting property."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class AgentSettingProperty(BaseModel):
    """Represents a single setting property for an agent."""

    name: str = Field(default="", description="The name of the setting.")
    value: str = Field(default="", description="The value of the setting.")
    type: str = Field(default="string", description="The type of the setting value.")
    required: bool = Field(default=False, description="Whether the setting is required.")
    description: Optional[str] = Field(default=None, description="The description of the setting.")
    default_value: Optional[str] = Field(
        default=None, alias="defaultValue", description="The default value of the setting."
    )

    model_config = {"populate_by_name": True}
