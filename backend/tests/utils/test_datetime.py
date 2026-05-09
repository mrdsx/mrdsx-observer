from datetime import datetime

from src.utils.datetime import isodate


def test_isodate():
    assert isodate(datetime(2020, 1, 1)) == "2020-01-01"
    assert isodate(datetime(999, 1, 15)) == "0999-01-15"
    assert isodate(datetime(2026, 12, 31)) == "2026-12-31"
