import httpx
from fastapi import FastAPI
from fastapi_crons import Crons, get_cron_router

from api import api_router
from api.dependencies import get_firestore
from core.constants import LOGGING_INTERVAL_MINUTES
from lifespan import lifespan
from services.olympiad_preparation import (
    capture_olympiad_preparation,
)

app = FastAPI(lifespan=lifespan)
crons = Crons(app)


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
