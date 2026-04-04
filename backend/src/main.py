import asyncio

import httpx
from fastapi import FastAPI
from fastapi_crons import Crons, get_cron_router

from api.dependencies import get_firestore
from api import api_router
from lifespan import lifespan
from services.olympiad_preparation import capture_api, capture_static_assets

app = FastAPI(lifespan=lifespan)
crons = Crons(app)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(api_router)
app.include_router(get_cron_router())


@crons.cron("*/5 * * * *", name="capture_projects_uptime")
async def capture_projects_uptime():
    db = get_firestore()

    async with httpx.AsyncClient() as client:
        static_assets_coro = capture_static_assets(client, db)
        api_coro = capture_api(client, db)

        await asyncio.gather(static_assets_coro, api_coro)
