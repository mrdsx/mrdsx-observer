from datetime import datetime
from typing import Any

import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.api.dependencies import get_projects_reports_repository
from src.core.settings import get_settings
from src.models.projects_reports import DB_DailyProjectReport
from src.schemas.projects_reports import ProjectServiceReport
from src.utils.db import deserialize_rows

settings = get_settings()


@pytest.mark.asyncio
async def test_fetch_reports_for_period(
    session: AsyncSession,
    raw_daily_reports: list[dict[str, Any]],
):
    # test without refresh
    projects_reports_repository = get_projects_reports_repository()

    # TODO: move db reports to fixture
    session.add_all([DB_DailyProjectReport(**report) for report in raw_daily_reports])
    raw_reports = await projects_reports_repository.fetch_reports_for_period(
        start_date=datetime(year=2026, month=1, day=1),
        end_date=datetime(year=2027, month=1, day=2),
        session=session,
    )
    assert len(raw_reports) == 4

    await session.execute(delete(DB_DailyProjectReport))
    raw_reports = await projects_reports_repository.fetch_reports_for_period(
        start_date=datetime(year=2026, month=1, day=1),
        end_date=datetime(year=2027, month=1, day=2),
        session=session,
    )
    assert len(raw_reports) == 4

    # test with refresh
    session.add_all([DB_DailyProjectReport(**report) for report in raw_daily_reports])
    raw_reports = await projects_reports_repository.fetch_reports_for_period(
        start_date=datetime(year=2026, month=1, day=1),
        end_date=datetime(year=2027, month=1, day=2),
        session=session,
        force_refresh=True,  # pyright: ignore[reportCallIssue]
    )
    assert len(raw_reports) == 4

    await session.execute(delete(DB_DailyProjectReport))
    raw_reports = await projects_reports_repository.fetch_reports_for_period(
        start_date=datetime(year=2026, month=1, day=1),
        end_date=datetime(year=2027, month=1, day=2),
        session=session,
        force_refresh=True,  # pyright: ignore[reportCallIssue]
    )
    assert len(raw_reports) == 0


@pytest.mark.asyncio
async def test_fetch_reports_by_day(
    session: AsyncSession,
    raw_daily_reports: list[dict[str, Any]],
    first_project1_report: dict[str, Any],
    first_project2_report: dict[str, Any],
):
    projects_reports_repository = get_projects_reports_repository()

    session.add_all([DB_DailyProjectReport(**report) for report in raw_daily_reports])
    raw_reports = await projects_reports_repository.fetch_reports_by_day(
        current_date=datetime(year=2027, month=1, day=1),
        session=session,
    )
    assert raw_reports == [first_project1_report, first_project2_report]


@pytest.mark.asyncio
async def test_insert_report(
    session: AsyncSession,
    first_project1_report: dict[str, Any],
):
    projects_reports_repository = get_projects_reports_repository()

    await projects_reports_repository.insert_report(
        project_id="project1",
        current_date=datetime(year=2027, month=1, day=1),
        services_reports={
            "service": ProjectServiceReport(
                current_status="operational",
                operational=1,
                degraded=0,
                outages=0,
            )
        },
        session=session,
    )
    result = await session.execute(select(DB_DailyProjectReport))
    raw_reports = deserialize_rows(result)
    assert raw_reports == [first_project1_report]


@pytest.mark.asyncio
async def test_update_report(
    session: AsyncSession,
    raw_daily_reports: list[dict[str, Any]],
):
    projects_reports_repository = get_projects_reports_repository()

    session.add_all([DB_DailyProjectReport(**report) for report in raw_daily_reports])
    result = await session.execute(select(DB_DailyProjectReport))
    raw_reports = deserialize_rows(result)
    assert len(raw_reports) == len(raw_daily_reports)
    assert raw_reports[-1] == {
        "project_id": "project2",
        "date_str": "2027-01-02",
        "created_at": datetime(year=2027, month=1, day=2),
        "services_reports": {
            "service": {
                "current_status": "degraded",
                "operational": 0,  # this field WILL BE updated
                "degraded": 1,
                "outages": 0,
            }
        },
    }

    await projects_reports_repository.update_report(
        project_id="project2",
        current_date=datetime(year=2027, month=1, day=2),
        services_reports={
            "service": ProjectServiceReport(
                current_status="operational",
                operational=2,
                degraded=1,
                outages=0,
            )
        },
        session=session,
    )
    result = await session.execute(select(DB_DailyProjectReport))
    raw_reports = deserialize_rows(result)
    assert len(raw_reports) == len(raw_daily_reports)
    assert raw_reports[-1] == {
        "project_id": "project2",
        "date_str": "2027-01-02",
        "created_at": datetime(year=2027, month=1, day=2),
        "services_reports": {
            "service": {
                "current_status": "operational",
                "operational": 2,  # this field IS updated
                "degraded": 1,
                "outages": 0,
            }
        },
    }


@pytest.mark.asyncio
async def test_delete_old_reports(
    session: AsyncSession,
    raw_daily_reports: list[dict[str, Any]],
    second_project1_report: dict[str, Any],
    second_project2_report: dict[str, Any],
):
    projects_reports_repository = get_projects_reports_repository()

    session.add_all([DB_DailyProjectReport(**report) for report in raw_daily_reports])
    result = await session.execute(select(DB_DailyProjectReport))
    assert len(result.scalars().all()) == len(raw_daily_reports)

    await projects_reports_repository.delete_old_reports(
        cutoff_date=datetime(year=2027, month=1, day=2), session=session
    )
    result = await session.execute(select(DB_DailyProjectReport))
    raw_reports = deserialize_rows(result)
    assert raw_reports == [second_project1_report, second_project2_report]
