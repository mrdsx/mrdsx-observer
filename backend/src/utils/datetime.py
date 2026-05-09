from datetime import datetime


def isodate(date: datetime) -> str:
    """Returns date string: YYYY-MM-DD."""

    return date.date().isoformat()
