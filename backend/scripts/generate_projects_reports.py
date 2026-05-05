import asyncio
import random
import sys
from datetime import timedelta

from google.api_core.datetime_helpers import DatetimeWithNanoseconds

sys.path.append("./")

from src.api.dependencies import get_firestore
from src.core.constants import FirestoreKeys
from src.core.firebase import initialize_firebase
from src.core.types import ServiceStatus
from src.schemas.projects_reports import (
    DailyProjectsReport,
    ProjectReport,
    ProjectServiceReport,
)
from src.utils.datetime import isodate

initialize_firebase()

TIME_WINDOW_DAYS = 40


def get_random_status() -> ServiceStatus:
    value = random.randint(1, 100)
    if value > 98:
        return "outage"
    elif value > 90:
        return "degraded"
    return "operational"


async def generate_reports() -> None:
    firestore = get_firestore()
    projects = [
        ("classic-word-game", "Classic word game", ("API", "Site")),
        ("mrdsx-observer", "mrdsx observer", ("Site",)),
        (
            "olympiad-preparation",
            "Olympiad Preparation",
            ("API", "Site", "Static Assets"),
        ),
        ("swift-tracker", "Swift Tracker", ("Site",)),
    ]

    # time window (magic number)
    for days_offset in range(TIME_WINDOW_DAYS):
        current_date = DatetimeWithNanoseconds.now() - timedelta(days=days_offset)
        doc_id = isodate(current_date)
        doc_ref = firestore.collection(FirestoreKeys.PROJECTS_REPORTS).document(doc_id)
        daily_report = DailyProjectsReport(created_at=current_date, projects={})

        for project_id, project_name, services in projects:
            project_report = ProjectReport(name=project_name, services={})
            for service in services:
                service_status = get_random_status()
                project_report.services[service] = ProjectServiceReport(
                    current_status=service_status,
                    operational=1 if service_status == "operational" else 0,
                    degraded=1 if service_status == "degraded" else 0,
                    outages=1 if service_status == "outage" else 0,
                )
            daily_report.projects[project_id] = project_report

        await doc_ref.set(daily_report.model_dump())

        print(f"Created report with doc_id: {doc_id}")


asyncio.run(generate_reports())
