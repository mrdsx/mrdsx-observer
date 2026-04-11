import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from redis.asyncio import Redis

from src.api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
    get_projects_reports_service,
    get_redis,
)
from src.core.constants import CACHE_TTL_SECONDS, RedisKeys
from src.core.firebase.types import AsyncFirestore
from src.repositories.projects_reports import ProjectsReportsRepository
from src.schemas.projects_reports import ProjectsReportsOut
from src.services.projects_reports import ProjectsReportsService

router = APIRouter(prefix="/projects")


@router.get("/")
async def get_projects_reports(
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    redis: Annotated[Redis, Depends(get_redis)],
    reports_service: Annotated[
        ProjectsReportsService, Depends(get_projects_reports_service)
    ],
    reports_repository: Annotated[
        ProjectsReportsRepository,
        Depends(get_projects_reports_repository),
    ],
) -> ProjectsReportsOut:
    try:
        cached_reports = await redis.get(RedisKeys.PROJECTS_REPORTS)
        if cached_reports is not None:
            return ProjectsReportsOut.model_validate_json(cached_reports)
    except ValidationError, json.JSONDecodeError:
        pass

    projects_reports = await reports_service.get_projects_reports(
        reports_repository=reports_repository, db=db
    )

    await redis.set(
        RedisKeys.PROJECTS_REPORTS,
        projects_reports.model_dump_json(),
        ex=CACHE_TTL_SECONDS,
    )

    return projects_reports


@router.get("/{project_id}")
async def get_project_report(project_id: str) -> dict[str, Any]:
    return {"status": "ok"}
