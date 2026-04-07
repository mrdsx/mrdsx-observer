import asyncio
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crons import Crons, get_cron_router

from src.api import api_router
from src.api.dependencies import get_firestore
from src.core.constants import LOGGING_INTERVAL_MINUTES
from src.core.settings import get_settings
from src.lifespan import lifespan
from src.services.projects import (
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


@app.get("/", response_model=dict[str, Any])
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
