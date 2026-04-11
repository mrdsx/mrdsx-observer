import asyncio
from datetime import datetime
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crons import Crons
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from api import api_router
from api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
    get_projects_reports_service,
    get_redis,
)
from core.constants import (
    CACHE_TTL_SECONDS,
    LOGGING_INTERVAL_MINUTES,
    FirestoreKeys,
    RedisKeys,
)
from core.settings import get_settings
from core.types import ServiceStatus
from lifespan import lifespan
from schemas.projects_reports import (
    DailyProjectsReport,
    ProjectReport,
    ProjectServiceReport,
)
from services.projects_reports import (
    ProjectsStateSnapshotter,
)
from utils.datetime import isodate

settings = get_settings()


def get_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_methods=["GET"],
    )

    @_app.get("/")
    async def root() -> dict[str, Any]:
        return {"status": "ok"}

    _app.include_router(api_router)

    return _app


app = get_app()
crons = Crons(app)


@crons.cron(f"*/{LOGGING_INTERVAL_MINUTES} * * * *")
async def report_projects_status():
    db = get_firestore()
    redis = get_redis()
    snapshotter = ProjectsStateSnapshotter()
    reports_repository = get_projects_reports_repository()
    reports_service = get_projects_reports_service()

    async with httpx.AsyncClient() as http_client:
        async with asyncio.TaskGroup() as task_group:
            task1 = task_group.create_task(
                snapshotter.capture_olympiad_preparation(http_client=http_client)
            )
            task2 = task_group.create_task(
                snapshotter.capture_classic_word_game(http_client=http_client)
            )

    report_ref = db.document(
        FirestoreKeys.PROJECTS_REPORTS,
        isodate(datetime.now()),
    )
    report_doc = await report_ref.get()
    raw_report = report_doc.to_dict()
    if raw_report is None:
        raw_report = {
            "created_at": DatetimeWithNanoseconds.now(),
            "projects": {},
        }

    projects_status: list[tuple[str, str, dict[str, ServiceStatus]]] = [
        ("olympiad-preparation", "Olympiad Preparation", task1.result()),
        ("classic-word-game", "Classic word game", task2.result()),
    ]
    daily_report = DailyProjectsReport.model_validate(raw_report)

    for project_id, project_name, services_status in projects_status:
        project = daily_report.projects.get(project_id)
        if project is None:
            services_reports: dict[str, ProjectServiceReport] = {}

            for service_name, service_status in services_status.items():
                operational = 1 if service_status == "operational" else 0
                degraded = 1 if service_status == "degraded" else 0
                outages = 1 if service_status == "outage" else 0

                services_reports[service_name] = ProjectServiceReport(
                    current_status=service_status,
                    operational=operational,
                    degraded=degraded,
                    outages=outages,
                )

            daily_report.projects[project_id] = ProjectReport(
                name=project_name,
                services=services_reports,
            )
        else:
            services_reports: dict[str, ProjectServiceReport] = project.services

            for service_name, service_status in services_status.items():
                service_details = services_reports.get(service_name)
                if service_details is None:
                    operational = 1 if service_status == "operational" else 0
                    degraded = 1 if service_status == "degraded" else 0
                    outages = 1 if service_status == "outage" else 0

                    services_reports[service_name] = ProjectServiceReport(
                        current_status=service_status,
                        operational=operational,
                        degraded=degraded,
                        outages=outages,
                    )
                else:
                    services_reports[service_name].current_status = service_status
                    if service_status == "operational":
                        services_reports[service_name].operational += 1
                    elif service_status == "degraded":
                        services_reports[service_name].degraded += 1
                    elif service_status == "outage":
                        services_reports[service_name].outages += 1

    await report_ref.set(daily_report.model_dump())

    projects_reports = await reports_service.get_projects_reports(
        reports_repository=reports_repository, db=db
    )
    await redis.set(
        name=RedisKeys.PROJECTS_REPORTS,
        value=projects_reports.model_dump_json(),
        ex=CACHE_TTL_SECONDS,
    )
