import json
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from redis.asyncio import Redis

from src.api.dependencies import get_firestore, get_redis
from src.core.constants import CACHE_TTL_SECONDS, RedisKeys
from src.core.firebase.types import AsyncFirestore
from src.schemas.projects_logs import ProjectsReportsOut
from src.services.projects_logs import (
    get_projects_logs,
    map_projects_reports,
    normalize_projects_reports,
)
from src.utils.projects_logs import projects_logs_range

router = APIRouter(prefix="/projects")


@router.get("/")
async def get_projects_reports(
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    redis: Annotated[Redis, Depends(get_redis)],
) -> ProjectsReportsOut:
    try:
        cached_reports = await redis.get(RedisKeys.PROJECTS_REPORTS)
        if cached_reports is not None:
            return ProjectsReportsOut(projects=json.loads(cached_reports))
    except ValidationError, json.JSONDecodeError:
        pass

    start_date, end_date = projects_logs_range()
    db_logs = await get_projects_logs(db, start_date, end_date)
    projects_details = normalize_projects_reports(db_logs)
    projects_data = map_projects_reports(projects_details)

    await redis.set(
        RedisKeys.PROJECTS_REPORTS,
        json.dumps(projects_data),
        ex=CACHE_TTL_SECONDS,
    )
    return ProjectsReportsOut(projects=projects_data)  # pyright: ignore[reportArgumentType]


@router.get("/{project_id}")
async def get_project_report(project_id: str):
    return {"status": "ok"}
