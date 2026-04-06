import asyncio

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crons import Crons, get_cron_router

from api import api_router
from api.dependencies import get_firestore
from core.constants import LOGGING_INTERVAL_MINUTES
from core.settings import get_settings
from lifespan import lifespan
from services.projects import (
    capture_classic_word_game,
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
        coro1 = capture_olympiad_preparation(client, db)
        coro2 = capture_classic_word_game(client, db)

        await asyncio.gather(coro1, coro2)
