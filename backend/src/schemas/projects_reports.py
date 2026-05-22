from datetime import datetime
from typing import Self

from pydantic import BaseModel, NonNegativeInt, model_validator

from src.core.types import ServiceStatus
from src.schemas.api import api_model_config, uptime_field
from src.utils.datetime import isodate


class DailyProjectReport(BaseModel):
    date_str: str
    created_at: datetime
    project_id: str
    services_reports: dict[str, ProjectServiceReport]

    @model_validator(mode="after")
    def date_fields_match(self) -> Self:
        if self.date_str != isodate(self.created_at):
            raise ValueError("fields 'date_str' and 'created_at' must match")
        return self

    @model_validator(mode="after")
    def validate_services_reports(self) -> Self:
        for service_name, service_report in self.services_reports.items():
            current_status = service_report.current_status
            if (
                (current_status == "operational" and service_report.operational <= 0)
                or (current_status == "degraded" and service_report.degraded <= 0)
                or (current_status == "outage" and service_report.outages <= 0)
            ):
                raise ValueError(
                    f"{service_name} is {current_status} but corresponding status count is 0 or less."
                )

        return self


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
