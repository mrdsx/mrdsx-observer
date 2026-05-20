import asyncio
from datetime import datetime, timedelta

from src.api.dependencies import (
    get_projects_reports_repository,
)
from src.api.dependencies.session import get_session
from src.core.constants import REPORTS_RETENTION_WINDOW_DAYS
from src.models import initialize_db
from src.utils.datetime import midnight


async def delete_old_projects_reports() -> None:
    await initialize_db()
    projects_reports_repository = get_projects_reports_repository()

    cutoff_date = midnight(
        datetime.now() - timedelta(days=REPORTS_RETENTION_WINDOW_DAYS - 1)
    )
    async for session in get_session():
        await projects_reports_repository.delete_old_reports(
            cutoff_date=cutoff_date, session=session
        )

    print("Successfully deleted old projects reports.")


if __name__ == "__main__":
    asyncio.run(delete_old_projects_reports())
