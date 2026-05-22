from datetime import datetime
from typing import Any

import pytest
from freezegun import freeze_time

from src.utils.projects_reports import (
    projects_reports_range,
    validate_daily_reports,
    worst_status,
)


@pytest.fixture(scope="module")
def raw_daily_reports() -> list[dict[str, Any]]:
    return [
        {
            "id": 1,
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
            "id": 2,
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
            "id": 3,
            "date_str": "2027-01-01",
            "created_at": datetime(year=2027, month=1, day=1),
            "project_id": "project3",
            "services_reports": {
                "service": {
                    "current_status": "outage",
                    "operational": 0,
                    "degraded": 0,
                    "outages": 1,
                }
            },
        },
    ]


@freeze_time("2027-01-01")
def test_projects_reports_range():
    range = projects_reports_range(days=30)
    assert range[0] == datetime(
        year=2026, month=12, day=3, hour=0, minute=0, second=0, microsecond=0
    )
    assert range[1] == datetime(
        year=2027, month=1, day=1, hour=23, minute=59, second=59, microsecond=999999
    )

    range2 = projects_reports_range(days=90)
    assert range2[0] == datetime(
        year=2026, month=10, day=4, hour=0, minute=0, second=0, microsecond=0
    )
    assert range2[1] == datetime(
        year=2027, month=1, day=1, hour=23, minute=59, second=59, microsecond=999999
    )


def test_validate_daily_reports(raw_daily_reports: list[dict[str, Any]]):
    validate_daily_reports(raw_daily_reports)


def test_worst_status():
    assert worst_status("operational", "operational") == "operational"
    assert worst_status("operational", "degraded") == "degraded"
    assert worst_status("operational", "outage") == "outage"
    assert worst_status("outage", "degraded") == "outage"
    assert worst_status("outage", "outage") == "outage"
    assert worst_status("outage", "operational", "degraded") == "outage"
