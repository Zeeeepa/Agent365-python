from typing import Literal
from microsoft_agents.activity.entity import Entity


class EmailResponse(Entity):
    type: Literal["emailResponse"] = "emailResponse"
    html_body: str = ""
