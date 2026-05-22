from typing import Any

from sqlalchemy import Result


def deserialize_rows(result: Result) -> list[dict[str, Any]]:
    return [
        {column.name: getattr(row, column.name) for column in row.__table__.columns}
        for row in result.scalars().all()
    ]
