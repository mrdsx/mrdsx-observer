from datetime import datetime, time, timedelta

from core.constants import LOGS_WINDOW_DAYS
from core.types import ServiceStatus


def projects_logs_range(days: int = LOGS_WINDOW_DAYS) -> tuple[datetime, datetime]:
    now = datetime.now()
    # we substract one day because time window includes current day
    start_date = (now - timedelta(days=days - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = datetime.combine(now.date(), time.max)

    return (start_date, end_date)


def worst_status(*statuses: ServiceStatus) -> ServiceStatus:
    statuses_set = set(statuses)
    if "outage" in statuses_set:
        return "outage"
    elif "degraded" in statuses_set:
        return "degraded"
    return "operational"
