from dataclasses import dataclass

from core.types import ServiceStatus


@dataclass(slots=True)
class ProjectStatusDTO:
    uptime_percentage: float
    worst_status: ServiceStatus
    services_status: set[ServiceStatus]
    good_statuses: int
    outages: int


@dataclass
class ProjectReportDTO:
    name: str
    daily_reports: dict[str, DailyProjectReportDTO]
    current_status: ServiceStatus | None = None
    uptime: float | None = None


@dataclass
class DailyProjectReportDTO:
    worst_status: ServiceStatus
    uptime: float
