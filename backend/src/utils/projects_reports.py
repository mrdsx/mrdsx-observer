from datetime import datetime, time, timedelta

from src.core.constants import REPORTS_RETENTION_WINDOW_DAYS
from src.core.types import ServiceStatus


def projects_reports_range(
    days: int = REPORTS_RETENTION_WINDOW_DAYS,
) -> tuple[datetime, datetime]:
    now = datetime.now()
    # we substract one day because time window includes current day
    start_date = (now - timedelta(days=days - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = datetime.combine(now.date(), time.max)

    return (start_date, end_date)


def worst_status(*statuses: ServiceStatus) -> ServiceStatus:
    for status in statuses:
        if status == "outage":
            return "outage"
        elif status == "degraded":
            return "degraded"

    return "operational"
