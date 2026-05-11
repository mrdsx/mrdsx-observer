from dataclasses import dataclass

from google.api_core.datetime_helpers import DatetimeWithNanoseconds

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
    created_at: DatetimeWithNanoseconds
    current_status: ServiceStatus
    good_statuses: int
    total_statuses: int
