import json
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from redis.asyncio import Redis

from api.dependencies import get_firestore, get_redis
from core.constants import CACHE_TTL_SECONDS
from core.firebase.types import AsyncFirestore
from core.settings import get_settings
from schemas.projects_logs import ProjectsReportsOut
from services.projects_logs import (
    get_projects_logs,
    normalize_projects_reports,
    projects_logs_range,
    projects_reports_dict,
)

router = APIRouter(prefix="/projects")

settings = get_settings()


@router.get("/")
async def get_projects_reports(
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    redis: Annotated[Redis, Depends(get_redis)],
) -> ProjectsReportsOut:
    try:
        cached_reports = await redis.get("backend:projects_reports")
        if cached_reports is not None:
            return ProjectsReportsOut(projects=json.loads(cached_reports))
    except ValidationError, json.JSONDecodeError:
        pass

    start_date, end_date = projects_logs_range()
    db_logs = await get_projects_logs(db, start_date, end_date)
    projects_details = projects_reports_dict(db_logs)
    projects_data = normalize_projects_reports(projects_details)

    await redis.set(
        "backend:projects_reports",
        json.dumps(projects_data),
        ex=CACHE_TTL_SECONDS,
    )
    return ProjectsReportsOut(projects=projects_data)  # pyright: ignore[reportArgumentType]


@router.get("/{project_id}")
async def get_project_report(project_id: str):
    return {"status": "ok"}
