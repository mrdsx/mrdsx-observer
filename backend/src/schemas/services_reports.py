from pydantic import BaseModel

from src.core.types import ServiceStatus
from src.schemas.api import api_model_config, uptime_field


class ServicesReportsOut(BaseModel):
    project_name: str
    services: list[ServiceReportOut]

    model_config = api_model_config


class ServiceReportOut(BaseModel):
    name: str
    current_status: ServiceStatus
    uptime: float = uptime_field
    daily_reports: list[DailyServiceReportOut]

    model_config = api_model_config


class DailyServiceReportOut(BaseModel):
    date: str
    worst_status: ServiceStatus
    uptime: float = uptime_field

    model_config = api_model_config
