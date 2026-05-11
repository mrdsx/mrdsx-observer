import json
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from redis.asyncio import Redis

from src.api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
    get_projects_reports_service,
    get_redis,
    get_services_reports_service,
)
from src.core.constants import CACHE_TTL_SECONDS, RedisKeys
from src.core.firebase.types import AsyncFirestore
from src.repositories.projects_reports import ProjectsReportsRepository
from src.schemas.projects_reports import ProjectsReportsOut
from src.schemas.services_reports import ServicesReportsOut
from src.services.projects_reports import ProjectsReportsService
from src.services.services_reports import ServicesReportsService

router = APIRouter(prefix="/projects")


@router.get("/")
async def get_projects_reports(
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    redis: Annotated[Redis, Depends(get_redis)],
    projects_reports_service: Annotated[
        ProjectsReportsService,
        Depends(get_projects_reports_service),
    ],
    projects_reports_repository: Annotated[
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

    projects_reports = await projects_reports_service.get_projects_reports(
        projects_reports_repository=projects_reports_repository,
        db=db,
    )

    await redis.set(
        RedisKeys.PROJECTS_REPORTS,
        projects_reports.model_dump_json(),
        ex=CACHE_TTL_SECONDS,
    )

    return projects_reports


@router.get("/{project_slug}")
async def get_project_services_reports(
    project_slug: str,
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    redis: Annotated[Redis, Depends(get_redis)],
    projects_reports_repository: Annotated[
        ProjectsReportsRepository,
        Depends(get_projects_reports_repository),
    ],
    services_reports_service: Annotated[
        ServicesReportsService,
        Depends(get_services_reports_service),
    ],
) -> ServicesReportsOut:
    try:
        cached_reports = await redis.get(RedisKeys.PROJECT_REPORTS(project_slug))
        if cached_reports is not None:
            return ServicesReportsOut.model_validate_json(cached_reports)
    except ValidationError, json.JSONDecodeError:
        pass

    services_reports = await services_reports_service.get_services_reports(
        project_slug=project_slug,
        projects_reports_repository=projects_reports_repository,
        db=db,
    )

    await redis.set(
        RedisKeys.PROJECT_REPORTS(project_slug),
        services_reports.model_dump_json(),
        ex=CACHE_TTL_SECONDS,
    )

    return services_reports
