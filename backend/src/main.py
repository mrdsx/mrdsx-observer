from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crons import Crons

from src.api import api_router
from src.api.dependencies import (
    get_firestore,
    get_projects_reports_repository,
)
from src.core.constants import (
    LOGGING_INTERVAL_MINUTES,
)
from src.core.settings import get_settings
from src.services.projects_reports import (
    DailyProjectsReportUpdater,
    ProjectsStateSnapshotter,
)
from src.utils.projects_reports import projects_reports_range

from .lifespan import lifespan

settings = get_settings()


def get_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
    )

    @_app.get("/")
    async def root() -> dict[str, Any]:
        return {"status": "ok"}

    _app.include_router(api_router)

    return _app


app = get_app()
crons = Crons(app)


# every X minutes
@crons.cron(f"*/{LOGGING_INTERVAL_MINUTES} * * * *")
async def report_projects_status() -> None:
    db = get_firestore()
    snapshotter = ProjectsStateSnapshotter()
    daily_report_updater = DailyProjectsReportUpdater()
    projects_reports_repository = get_projects_reports_repository()

    async with httpx.AsyncClient(proxy=settings.proxy_url) as http_client:
        await daily_report_updater.update_daily_report(
            snapshotter=snapshotter,
            http_client=http_client,
            db=db,
        )

    start_date, end_date = projects_reports_range()
    await projects_reports_repository.fetch_reports(
        start_date=start_date,
        end_date=end_date,
        db=db,
        force_refresh=True,  # pyright: ignore[reportCallIssue]
    )


# every day at midnight
@crons.cron("0 0 * * *")
async def delete_old_reports() -> None:
    db = get_firestore()
    reports_repository = get_projects_reports_repository()

    cutoff_date, _ = projects_reports_range()
    await reports_repository.delete_old_reports(
        cutoff_date=cutoff_date,
        db=db,
    )
