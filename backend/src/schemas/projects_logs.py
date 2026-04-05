from typing import Any

from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from core.types import ServiceStatus


class ProjectLog(BaseModel):
    project_id: str
    project_name: str
    timestamp: Any
    components: dict[str, ServiceStatus]


class ProjectLogInDB(ProjectLog):
    timestamp: DatetimeWithNanoseconds

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DailyProjectReportOut(BaseModel):
    worst_status: ServiceStatus
    uptime: float = Field(ge=0, le=100)
    date: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_alias=True,
        validate_by_name=True,
    )


class ProjectReportOut(BaseModel):
    id: str
    name: str
    status: ServiceStatus
    uptime: float = Field(ge=0, le=100)
    daily_reports: list[DailyProjectReportOut]

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_alias=True,
        validate_by_name=True,
    )


class ProjectsReportsOut(BaseModel):
    projects: list[ProjectReportOut]

    model_config = ConfigDict(alias_generator=to_camel)
