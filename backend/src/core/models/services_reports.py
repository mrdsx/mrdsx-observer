from dataclasses import dataclass
from datetime import datetime

from src.core.types import ServiceStatus


@dataclass(slots=True)
class DailyServiceReportDTO:
    worst_status: ServiceStatus
    uptime: float


@dataclass
class ServiceReportsDTO:
    daily_reports: dict[str, DailyServiceReportDTO]
    current_status: ServiceStatus | None = None
    uptime: float | None = None


@dataclass(slots=True)
class LatestServiceStatusDTO:
    created_at: datetime
    current_status: ServiceStatus
    good_statuses: int
    total_statuses: int
