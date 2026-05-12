import asyncio
from datetime import datetime, timedelta

from src.api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
)
from src.core.constants import REPORTS_RETENTION_WINDOW_DAYS
from src.core.firebase import initialize_firebase


async def delete_old_projects_reports() -> None:
    initialize_firebase()
    db = get_firestore()
    projects_reports_repository = get_projects_reports_repository()

    cutoff_date = (
        datetime.now() - timedelta(days=REPORTS_RETENTION_WINDOW_DAYS - 1)
    ).replace(hour=0, minute=0, second=0, microsecond=0)
    await projects_reports_repository.delete_old_reports(cutoff_date=cutoff_date, db=db)

    print("Successfully deleted old projects reports.")


asyncio.run(delete_old_projects_reports())
