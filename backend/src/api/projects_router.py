from collections import Counter
from datetime import datetime, time, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from google.cloud.firestore_v1.base_query import And, FieldFilter
from pydantic import TypeAdapter

from api.dependencies import get_firestore
from core.firebase.types import AsyncFirestore
from core.types import ServiceStatus
from schemas.projects_logs import ProjectLogInDB, ProjectsReportsOut
from utils.projects_logs import worst_status


router = APIRouter(prefix="/projects")


@router.get("/")
async def get_projects_reports(
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
) -> ProjectsReportsOut:
    now = datetime.now()
    start_date = (now - timedelta(days=29)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = datetime.combine(now.date(), time.max)

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
    projects_details: dict[str, dict[str, Any]] = {}

    for log in db_logs:
        date_str = log.timestamp.date().isoformat()
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
        else:
            existing_details["daily_reports"][date_str].append(worst_log_status)

    projects_data = []

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

    return ProjectsReportsOut(projects=projects_data)


@router.get("/{project_id}")
async def get_project_report(project_id: str):
    return {"status": "ok"}
