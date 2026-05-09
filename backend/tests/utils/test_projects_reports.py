from freezegun import freeze_time

from src.utils.projects_reports import projects_reports_range, worst_status


@freeze_time("2027-01-01")
def test_projects_reports_range():
    range = projects_reports_range(days=30)
    assert range[0].year == 2026
    assert range[0].month == 12
    assert range[0].day == 3
    assert range[1].year == 2027
    assert range[1].month == 1
    assert range[1].day == 1

    range2 = projects_reports_range(days=90)
    assert range2[0].year == 2026
    assert range2[0].month == 10
    assert range2[0].day == 4
    assert range2[1].year == 2027
    assert range2[1].month == 1
    assert range2[1].day == 1


def test_worst_status():
    assert worst_status("operational", "operational") == "operational"
    assert worst_status("operational", "degraded") == "degraded"
    assert worst_status("operational", "outage") == "outage"
    assert worst_status("outage", "degraded") == "outage"
    assert worst_status("outage", "outage") == "outage"
    assert worst_status("outage", "operational", "degraded") == "outage"
