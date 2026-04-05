from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from core.types import ServiceStatus


class ProjectLog(BaseModel):
    project_id: str
    project_name: str
    timestamp: Any
    components: list[ProjectComponent]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ProjectComponent(BaseModel):
    name: str
    status: ServiceStatus
