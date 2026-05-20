from datetime import datetime, time, timedelta
from typing import Any

from pydantic import TypeAdapter

from src.core.constants import REPORTS_RETENTION_WINDOW_DAYS
from src.core.types import ServiceStatus
from src.schemas.projects_reports import DailyProjectReport
from src.utils.datetime import midnight


def projects_reports_range(
    days: int = REPORTS_RETENTION_WINDOW_DAYS,
) -> tuple[datetime, datetime]:
    now = datetime.now()
    # we substract one day because time window includes current day
    start_date = midnight(now - timedelta(days=days - 1))
    end_date = datetime.combine(now.date(), time.max)

    return (start_date, end_date)


def worst_status(*statuses: ServiceStatus) -> ServiceStatus:
    for status in statuses:
        if status == "outage":
            return "outage"
        elif status == "degraded":
            return "degraded"

    return "operational"


def validate_daily_reports(reports: Any) -> list[DailyProjectReport]:
    adapter = TypeAdapter(list[DailyProjectReport])
    daily_reports = adapter.validate_python(reports)
    return daily_reports
