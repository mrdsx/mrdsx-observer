import asyncio
import random
from datetime import timedelta

from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from src.api.dependencies import get_firestore
from src.core.constants import FirestoreKeys
from src.core.firebase import initialize_firebase
from src.core.types import ServiceStatus
from src.schemas.projects_reports import (
    DailyProjectsReport,
    ProjectServiceReport,
)
from src.utils.datetime import isodate

TIME_WINDOW_DAYS = 40


def get_random_status() -> ServiceStatus:
    value = random.randint(1, 100)
    if value > 98:
        return "outage"
    elif value > 90:
        return "degraded"
    return "operational"


async def generate_projects_reports() -> None:
    initialize_firebase()
    db = get_firestore()

    projects = [
        ("classic-word-game", ["API", "Site"]),
        ("mrdsx-observer", ["Site"]),
        ("olympiad-preparation", ["API", "Site", "Static Assets"]),
        ("swift-tracker", ["Site"]),
    ]

    for days_offset in range(TIME_WINDOW_DAYS):
        current_date = DatetimeWithNanoseconds.now() - timedelta(days=days_offset)
        doc_id = isodate(current_date)
        doc_ref = db.collection(FirestoreKeys.PROJECTS_REPORTS).document(doc_id)
        daily_report = DailyProjectsReport(created_at=current_date, projects={})

        for project_id, services in projects:
            project_report = {}
            for service in services:
                service_status = get_random_status()
                project_report[service] = ProjectServiceReport(
                    current_status=service_status,
                    operational=1 if service_status == "operational" else 0,
                    degraded=1 if service_status == "degraded" else 0,
                    outages=1 if service_status == "outage" else 0,
                )
            daily_report.projects[project_id] = project_report

        await doc_ref.set(daily_report.model_dump())

        print(f"Created report with doc_id: {doc_id}")


asyncio.run(generate_projects_reports())
