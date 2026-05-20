from datetime import datetime

from pydantic import BaseModel

from src.schemas.projects_reports import ProjectServiceReport


class DailyProjectReport(BaseModel):
    id: int
    date_str: str
    created_at: datetime
    project_id: str
    services_reports: dict[str, ProjectServiceReport]
