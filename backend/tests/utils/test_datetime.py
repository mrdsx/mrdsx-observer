from datetime import datetime

from src.utils.datetime import isodate, midnight


def test_midnight():
    dt = datetime(year=2027, month=1, day=1, hour=1, minute=1, second=1, microsecond=1)
    assert midnight(dt).year == 2027
    assert midnight(dt).month == 1
    assert midnight(dt).day == 1
    assert midnight(dt).hour == 0
    assert midnight(dt).minute == 0
    assert midnight(dt).second == 0
    assert midnight(dt).microsecond == 0


def test_isodate():
    assert isodate(datetime(2020, 1, 1)) == "2020-01-01"
    assert isodate(datetime(999, 1, 15)) == "0999-01-15"
    assert isodate(datetime(2026, 12, 31)) == "2026-12-31"
