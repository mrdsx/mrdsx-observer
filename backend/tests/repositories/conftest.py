from typing import Any

import pytest

from src.models.projects_reports import DB_DailyProjectReport


@pytest.fixture
def db_daily_reports(
    raw_daily_reports: list[dict[str, Any]],
) -> list[DB_DailyProjectReport]:
    return [DB_DailyProjectReport(**report) for report in raw_daily_reports]
