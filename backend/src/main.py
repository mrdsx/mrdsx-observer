from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crons import Crons

from src.api import api_router
from src.api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
    get_projects_reports_service,
    get_redis,
)
from src.core.constants import (
    CACHE_TTL_SECONDS,
    LOGGING_INTERVAL_MINUTES,
    RedisKeys,
)
from src.core.settings import get_settings
from src.services.projects_reports import (
    DailyProjectsReportUpdater,
    ProjectsStateSnapshotter,
)

from .lifespan import lifespan

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
    snapshotter = ProjectsStateSnapshotter()
    daily_report_updater = DailyProjectsReportUpdater()
    reports_repository = get_projects_reports_repository()
    reports_service = get_projects_reports_service()
    db = get_firestore()
    redis = get_redis()

    async with httpx.AsyncClient() as http_client:
        await daily_report_updater.update_daily_report(
            snapshotter=snapshotter,
            http_client=http_client,
            db=db,
        )

    projects_reports = await reports_service.get_projects_reports(
        reports_repository=reports_repository,
        db=db,
    )
    await redis.set(
        name=RedisKeys.PROJECTS_REPORTS,
        value=projects_reports.model_dump_json(),
        ex=CACHE_TTL_SECONDS,
    )
