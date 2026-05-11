from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
    get_projects_reports_service,
    get_services_reports_service,
)
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
    projects_reports_service: Annotated[
        ProjectsReportsService,
        Depends(get_projects_reports_service),
    ],
    projects_reports_repository: Annotated[
        ProjectsReportsRepository,
        Depends(get_projects_reports_repository),
    ],
) -> ProjectsReportsOut:
    projects_reports = await projects_reports_service.get_projects_reports(
        projects_reports_repository=projects_reports_repository,
        db=db,
    )

    return projects_reports


@router.get("/{project_slug}")
async def get_project_services_reports(
    project_slug: str,
    db: Annotated[AsyncFirestore, Depends(get_firestore)],
    projects_reports_repository: Annotated[
        ProjectsReportsRepository,
        Depends(get_projects_reports_repository),
    ],
    services_reports_service: Annotated[
        ServicesReportsService,
        Depends(get_services_reports_service),
    ],
) -> ServicesReportsOut:
    services_reports = await services_reports_service.get_services_reports(
        project_slug=project_slug,
        projects_reports_repository=projects_reports_repository,
        db=db,
    )

    return services_reports
