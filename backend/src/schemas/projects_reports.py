from typing import Any

from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pydantic import BaseModel, ConfigDict, NonNegativeInt, field_validator

from src.core.types import ServiceStatus
from src.schemas.api import api_model_config, uptime_field


class DailyProjectsReport(BaseModel):
    created_at: DatetimeWithNanoseconds
    projects: dict[str, dict[str, ProjectServiceReport]]

    @field_validator("created_at", mode="before")
    @classmethod
    def normalize_date(cls, date: Any) -> Any:
        if isinstance(date, str):
            return DatetimeWithNanoseconds.fromisoformat(date)
        return date

    model_config = ConfigDict(arbitrary_types_allowed=True)


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
    uptime: float = uptime_field
    daily_reports: list[DailyProjectReportOut]

    model_config = api_model_config


class DailyProjectReportOut(BaseModel):
    worst_status: ServiceStatus
    uptime: float = uptime_field
    date: str

    model_config = api_model_config
