from datetime import datetime


def midnight(date: datetime) -> datetime:
    """Returns datetime object with time set to exactly 12 AM."""

    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def isodate(date: datetime) -> str:
    """Returns date string: YYYY-MM-DD."""

    return date.date().isoformat()
