import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy import delete

from src.api.dependencies import get_projects_reports_repository
from src.api.dependencies.session import get_session
from src.core.constants import REPORTS_RETENTION_WINDOW_DAYS
from src.core.types import ServiceStatus
from src.models.projects_reports import DB_DailyProjectReport
from src.schemas.projects_reports import ProjectServiceReport
from src.utils.datetime import isodate, midnight

TIME_WINDOW_DAYS = REPORTS_RETENTION_WINDOW_DAYS


def get_random_status() -> ServiceStatus:
    value = random.randint(1, 100)
    if value > 98:
        return "outage"
    elif value > 90:
        return "degraded"
    return "operational"


async def generate_projects_reports() -> None:
    projects_reports_repository = get_projects_reports_repository()

    projects = [
        ("classic-word-game", ["API", "Site"]),
        ("olympiad-preparation", ["API", "Site", "Static Assets"]),
        ("swift-tracker", ["Site"]),
    ]

    async for session in get_session():
        await session.execute(delete(DB_DailyProjectReport))

        # range [0, 29]
        for days_offset in range(TIME_WINDOW_DAYS):
            current_date = midnight(datetime.now() - timedelta(days=days_offset))
            date_str = isodate(current_date)

            for project_id, services in projects:
                services_reports: dict[str, ProjectServiceReport] = {}

                for service in services:
                    status = get_random_status()
                    services_reports[service] = ProjectServiceReport(
                        current_status=status,
                        operational=1 if status == "operational" else 0,
                        degraded=1 if status == "degraded" else 0,
                        outages=1 if status == "outage" else 0,
                    )

                await projects_reports_repository.insert_report(
                    project_id=project_id,
                    current_date=current_date,
                    services_reports=services_reports,
                    session=session,
                )

            print(f"Created report with {date_str=}")


if __name__ == "__main__":
    asyncio.run(generate_projects_reports())
