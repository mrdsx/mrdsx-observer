from typing import Annotated, Any

from fastapi import APIRouter, Depends

from api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
    get_projects_reports_service,
)
from core.firebase.types import AsyncFirestore
from repositories.projects_reports import ProjectsReportsRepository
from schemas.projects_reports import ProjectsReportsOut
from services.projects_reports import ProjectsReportsService

router = APIRouter(prefix="/projects")


@router.get("/")
async def get_projects_reports(
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    reports_service: Annotated[
        ProjectsReportsService, Depends(get_projects_reports_service)
    ],
    reports_repository: Annotated[
        ProjectsReportsRepository,
        Depends(get_projects_reports_repository),
    ],
) -> ProjectsReportsOut:
    # TODO: uncomment after testing in production
    # try:
    #     cached_reports = await redis.get(name=RedisKeys.PROJECTS_REPORTS)
    #     if cached_reports is not None:
    #         return ProjectsReportsOut(projects=json.loads(cached_reports))
    # except ValidationError, json.JSONDecodeError:
    #     pass

    projects_reports = await reports_service.get_projects_reports(
        reports_repository=reports_repository, db=db
    )

    # TODO: uncomment after testing in production
    # await redis.set(
    #     name=RedisKeys.PROJECTS_REPORTS,
    #     value=projects_reports.model_dump_json(),
    #     ex=CACHE_TTL_SECONDS,
    # )

    return projects_reports


@router.get("/{project_id}")
async def get_project_report(project_id: str) -> dict[str, Any]:
    return {"status": "ok"}
