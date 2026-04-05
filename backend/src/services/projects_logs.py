from collections import Counter
from datetime import datetime, time, timedelta
from typing import Any

from google.cloud.firestore_v1.base_query import And, FieldFilter
from pydantic import TypeAdapter

from core.constants import LOGS_WINDOW_DAYS
from core.firebase.types import AsyncFirestore
from core.types import ServiceStatus
from schemas.projects_logs import ProjectLogInDB
from utils.projects_logs import worst_status


async def get_projects_logs(
    db: AsyncFirestore,
    start_date: datetime,
    end_date: datetime,
) -> list[ProjectLogInDB]:
    projects_logs = db.collection("projects_logs")
    query = projects_logs.where(
        filter=And(
            [
                FieldFilter("timestamp", ">=", start_date),
                FieldFilter("timestamp", "<=", end_date),
            ]
        )
    ).order_by("timestamp", "DESCENDING")

    raw_logs = [doc.to_dict() async for doc in query.stream()]
    ta = TypeAdapter(list[ProjectLogInDB])
    db_logs = ta.validate_python(raw_logs)

    return db_logs


def projects_logs_range() -> tuple[datetime, datetime]:
    now = datetime.now()
    # with current day we would have 31 days window, so we substract 1 day
    start_date = (now - timedelta(days=LOGS_WINDOW_DAYS - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = datetime.combine(now.date(), time.max)

    return (start_date, end_date)


def projects_reports_dict(db_logs: list[ProjectLogInDB]) -> dict[str, dict[str, Any]]:
    projects_details: dict[str, dict[str, Any]] = {}

    for log in db_logs:
        date_str = log.timestamp.date().isoformat()  # yyyy-mm-dd
        worst_log_status = worst_status(*log.components.values())
        existing_details = projects_details.get(log.project_id)
        if existing_details is None:
            projects_details[log.project_id] = {
                "name": log.project_name,
                "status": worst_log_status,
                "daily_reports": {
                    date_str: [worst_log_status],
                },
            }
            continue

        existing_reports: list[ServiceStatus] | None = existing_details[
            "daily_reports"
        ].get(date_str)
        if existing_reports is None:
            existing_details["daily_reports"][date_str] = [worst_log_status]
        elif isinstance(existing_reports, list):
            existing_details["daily_reports"][date_str].append(worst_log_status)

    return projects_details


def normalize_projects_reports(
    projects_details: dict[str, dict[str, Any]],
):
    projects_data: list[dict[str, Any]] = []

    for project_id, rest_details in projects_details.items():
        final_reports = []
        reports: dict[str, list[ServiceStatus]] = rest_details["daily_reports"]
        total_outages = 0
        total_statuses = 0

        for date_str, statuses in reports.items():
            outages_count = Counter(statuses).get("outage", 0)
            statuses_count = len(statuses)
            good_statuses_count = statuses_count - outages_count
            uptime_percent = (good_statuses_count / statuses_count) * 100

            final_reports.append(
                {
                    "worst_status": worst_status(*statuses),
                    "uptime": round(uptime_percent, 2),
                    "date": date_str,
                }
            )
            total_outages += outages_count
            total_statuses += len(statuses)

        total_good_statuses = total_statuses - total_outages
        project_uptime_percent = (total_good_statuses / total_statuses) * 100
        rest_details["uptime"] = round(project_uptime_percent, 2)
        rest_details["daily_reports"] = final_reports
        projects_data.append({"id": project_id, **rest_details})

    return projects_data
