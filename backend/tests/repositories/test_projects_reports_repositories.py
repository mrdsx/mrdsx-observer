from datetime import datetime
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.api.dependencies import get_projects_reports_repository
from src.models.projects_reports import DB_DailyProjectReport


# TODO: extract to shared fixture
@pytest.fixture(scope="module")
def raw_daily_reports() -> list[dict[str, Any]]:
    return [
        {
            "date_str": "2027-01-01",
            "created_at": datetime(year=2027, month=1, day=1),
            "project_id": "project1",
            "services_reports": {
                "service": {
                    "current_status": "operational",
                    "operational": 1,
                    "degraded": 0,
                    "outages": 0,
                }
            },
        },
        {
            "date_str": "2027-01-01",
            "created_at": datetime(year=2027, month=1, day=1),
            "project_id": "project2",
            "services_reports": {
                "service": {
                    "current_status": "degraded",
                    "operational": 0,
                    "degraded": 1,
                    "outages": 0,
                }
            },
        },
        {
            "date_str": "2027-01-02",
            "created_at": datetime(year=2027, month=1, day=2),
            "project_id": "project1",
            "services_reports": {
                "service": {
                    "current_status": "outage",
                    "operational": 0,
                    "degraded": 0,
                    "outages": 1,
                }
            },
        },
        {
            "date_str": "2027-01-02",
            "created_at": datetime(year=2027, month=1, day=2),
            "project_id": "project2",
            "services_reports": {
                "service": {
                    "current_status": "degraded",
                    "operational": 0,
                    "degraded": 1,
                    "outages": 0,
                }
            },
        },
    ]


@pytest.mark.asyncio
async def test_delete_old_reports(
    session: AsyncSession, raw_daily_reports: list[dict[str, Any]]
):
    projects_reports_repository = get_projects_reports_repository()

    session.add_all([DB_DailyProjectReport(**report) for report in raw_daily_reports])
    result = await session.execute(select(DB_DailyProjectReport))
    assert len(result.scalars().all()) == 4

    await projects_reports_repository.delete_old_reports(
        cutoff_date=datetime(year=2027, month=1, day=2), session=session
    )
    result = await session.execute(select(DB_DailyProjectReport))
    assert len(result.scalars().all()) == 2
