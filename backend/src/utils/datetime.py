from datetime import datetime


def isodate(date: datetime) -> str:
    """Returns date: YYYY-MM-DD."""

    return date.date().isoformat()
