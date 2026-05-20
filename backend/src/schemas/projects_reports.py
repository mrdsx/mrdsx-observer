from datetime import datetime

from pydantic import BaseModel, NonNegativeInt

from src.core.types import ServiceStatus
from src.schemas.api import api_model_config, uptime_field


class DailyProjectReport(BaseModel):
    id: int
    date_str: str
    created_at: datetime
    project_id: str
    services_reports: dict[str, ProjectServiceReport]


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
