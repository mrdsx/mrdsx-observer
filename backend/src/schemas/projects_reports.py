from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt

from src.core.types import ServiceStatus
from src.schemas.api import api_model_config


class DailyProjectsReport(BaseModel):
    created_at: DatetimeWithNanoseconds
    projects: dict[str, ProjectReport]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ProjectReport(BaseModel):
    name: str
    services: dict[str, ProjectServiceReport]


class ProjectServiceReport(BaseModel):
    current_status: ServiceStatus
    operational: NonNegativeInt
    degraded: NonNegativeInt
    outages: NonNegativeInt


class ProjectsReportsOut(BaseModel):
    projects: list[ProjectReportOut]

    model_config = api_model_config


class ProjectReportOut(BaseModel):
    id: str
    name: str
    current_status: ServiceStatus
    uptime: float = Field(ge=0, le=100)
    daily_reports: list[DailyProjectReportOut]

    model_config = api_model_config


class DailyProjectReportOut(BaseModel):
    worst_status: ServiceStatus
    uptime: float = Field(ge=0, le=100)
    date: str

    model_config = api_model_config
