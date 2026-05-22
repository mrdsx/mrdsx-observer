from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.projects_reports import DB_DailyProjectReport
from src.utils.db import serialize_rows


@pytest.mark.asyncio
async def test_serialize_rows(session: AsyncSession):
    session.add(
        DB_DailyProjectReport(
            project_id="project1",
            date_str="2027-01-01",
            created_at=datetime(year=2027, month=1, day=1),
            services_reports={
                "service1": {
                    "current_status": "operational",
                    "operational": 1,
                    "degraded": 0,
                    "outages": 0,
                }
            },
        )
    )

    result = await session.execute(select(DB_DailyProjectReport))
    serialized = serialize_rows(result)

    assert serialized == [
        {
            "project_id": "project1",
            "date_str": "2027-01-01",
            "created_at": datetime(year=2027, month=1, day=1),
            "services_reports": {
                "service1": {
                    "current_status": "operational",
                    "operational": 1,
                    "degraded": 0,
                    "outages": 0,
                }
            },
        }
    ]
