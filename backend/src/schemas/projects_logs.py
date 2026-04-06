from typing import Any

from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel, ConfigDict, Field

from core.types import ServiceStatus
from schemas.api import api_model_config


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

    model_config = api_model_config


class ProjectReportOut(BaseModel):
    id: str
    name: str
    status: ServiceStatus
    uptime: float = Field(ge=0, le=100)
    daily_reports: list[DailyProjectReportOut]

    model_config = api_model_config


class ProjectsReportsOut(BaseModel):
    projects: list[ProjectReportOut]

    model_config = api_model_config
