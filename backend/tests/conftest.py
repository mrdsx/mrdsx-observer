from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.settings import get_settings
from src.models import Base

settings = get_settings()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def test_lifespan():
    settings.app_env = "test"
    yield
    ...


@pytest.fixture(scope="session")
def first_project1_report() -> dict[str, Any]:
    return {
        "project_id": "project1",
        "date_str": "2027-01-01",
        "created_at": datetime(year=2027, month=1, day=1),
        "services_reports": {
            "service": {
                "current_status": "operational",
                "operational": 1,
                "degraded": 0,
                "outages": 0,
            }
        },
    }


@pytest.fixture(scope="session")
def first_project2_report() -> dict[str, Any]:
    return {
        "project_id": "project2",
        "date_str": "2027-01-01",
        "created_at": datetime(year=2027, month=1, day=1),
        "services_reports": {
            "service": {
                "current_status": "degraded",
                "operational": 0,
                "degraded": 1,
                "outages": 0,
            }
        },
    }


@pytest.fixture(scope="session")
def second_project1_report() -> dict[str, Any]:
    return {
        "project_id": "project1",
        "date_str": "2027-01-02",
        "created_at": datetime(year=2027, month=1, day=2),
        "services_reports": {
            "service": {
                "current_status": "outage",
                "operational": 0,
                "degraded": 0,
                "outages": 1,
            }
        },
    }


@pytest.fixture(scope="session")
def second_project2_report() -> dict[str, Any]:
    return {
        "project_id": "project2",
        "date_str": "2027-01-02",
        "created_at": datetime(year=2027, month=1, day=2),
        "services_reports": {
            "service": {
                "current_status": "degraded",
                "operational": 0,
                "degraded": 1,
                "outages": 0,
            }
        },
    }


@pytest.fixture(scope="session")
def raw_daily_reports(
    first_project1_report: dict[str, Any],
    first_project2_report: dict[str, Any],
    second_project1_report: dict[str, Any],
    second_project2_report: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    First - created on jan 1, 2027.
    Second - created on jan 2, 2027.
    """

    return [
        first_project1_report,
        first_project2_report,
        second_project1_report,
        second_project2_report,
    ]


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.db_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
