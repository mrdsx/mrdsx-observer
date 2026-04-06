import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crons import Crons, get_cron_router

from api import api_router
from api.dependencies import get_firestore
from core.constants import LOGGING_INTERVAL_MINUTES
from core.settings import get_settings
from lifespan import lifespan
from services.olympiad_preparation import (
    capture_olympiad_preparation,
)

settings = get_settings()

app = FastAPI(lifespan=lifespan)
crons = Crons(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["GET"],
)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(api_router)
app.include_router(get_cron_router())


@crons.cron(f"*/{LOGGING_INTERVAL_MINUTES} * * * *")
async def log_projects_statuses():
    db = get_firestore()

    async with httpx.AsyncClient() as client:
        await capture_olympiad_preparation(client, db)
