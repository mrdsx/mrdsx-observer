from datetime import datetime
from typing import Any

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class DB_DailyProjectReport(Base):
    __tablename__ = "projects_reports"

    project_id: Mapped[str] = mapped_column(primary_key=True)
    date_str: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    services_reports: Mapped[dict[str, Any]] = mapped_column(JSON)
