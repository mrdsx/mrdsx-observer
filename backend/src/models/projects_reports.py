from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class DB_DailyProjectReport(Base):
    __tablename__ = "projects_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[str]
    date_str: Mapped[str]
    created_at: Mapped[datetime]
    services_reports: Mapped[dict[str, Any]] = mapped_column(JSON)
