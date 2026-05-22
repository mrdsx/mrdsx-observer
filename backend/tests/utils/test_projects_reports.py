from datetime import datetime

from freezegun import freeze_time

from src.utils.projects_reports import projects_reports_range, worst_status


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


def test_worst_status():
    assert worst_status("operational", "operational") == "operational"
    assert worst_status("operational", "degraded") == "degraded"
    assert worst_status("operational", "outage") == "outage"
    assert worst_status("outage", "degraded") == "outage"
    assert worst_status("outage", "outage") == "outage"
    assert worst_status("outage", "operational", "degraded") == "outage"
