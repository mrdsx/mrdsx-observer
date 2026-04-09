import json
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from redis.asyncio import Redis

from src.api.dependencies import get_firestore, get_redis
from src.core.constants import CACHE_TTL_SECONDS, RedisKeys
from src.core.firebase.types import AsyncFirestore
from src.schemas.projects_logs import ProjectsReportsOut
from src.services.projects_reports import (
    retrieve_projects_reports,
)

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

    projects_reports = await retrieve_projects_reports(db)

    await redis.set(
        RedisKeys.PROJECTS_REPORTS,
        json.dumps(projects_reports),
        ex=CACHE_TTL_SECONDS,
    )
    return ProjectsReportsOut(projects=projects_reports)  # pyright: ignore[reportArgumentType]


@router.get("/{project_id}")
async def get_project_report(project_id: str):
    return {"status": "ok"}
