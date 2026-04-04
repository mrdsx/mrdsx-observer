import httpx
from fastapi import FastAPI
from fastapi_crons import Crons, get_cron_router
from firebase_admin import firestore

from api.dependencies import get_firestore
from core.constants import MIN_RESPONSE_SECONDS
from lifespan import lifespan
from schemas.logs import Status

app = FastAPI(lifespan=lifespan)
crons = Crons(app)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(get_cron_router())


@crons.cron("*/5 * * * *", name="fetch_projects_uptime")
async def fetch_projects_uptime():
    db = get_firestore()

    async with httpx.AsyncClient() as client:
        # static assets
        response = await client.get("https://olympiad-preparation.vercel.app")
        status: Status = "operational"
        if (
            response.is_success or response.is_redirect
        ) and response.elapsed.seconds >= MIN_RESPONSE_SECONDS:
            status = "degraded"
        elif not (response.is_success or response.is_redirect):
            status = "outage"

        print(f"static assets status: {status}")
        project_logs = db.collection(
            "projects", "olympiad-preparation", "components", "static-assets", "logs"
        )
        await project_logs.add(
            {
                "timestamp": firestore.SERVER_TIMESTAMP,  # pyright: ignore[reportAttributeAccessIssue]
                "status": status,
            }
        )

        # API
        res1 = await client.get(
            "https://olympiad-preparation.vercel.app/api/math-problems?schoolGrade=1"
        )
        res2 = await client.get("https://olympiad-preparation.onrender.com/word-game")
        res3 = await client.get(
            "https://olympiad-preparation.vercel.app/api/matches?gridSize=3x4&schoolGrade=1&isFinalOlympiadStage=false"
        )
        status: Status = "operational"

        success_list = [
            res1.is_success or res1.is_redirect,
            res2.is_success or res2.is_redirect,
            res3.is_success or res3.is_redirect,
        ]
        elapsed_seconds_list = [
            res1.elapsed.seconds,
            res2.elapsed.seconds,
            res3.elapsed.seconds,
        ]
        if True not in success_list:
            status = "outage"
        elif False in success_list or any(
            t >= MIN_RESPONSE_SECONDS for t in elapsed_seconds_list
        ):
            status = "degraded"

        print(f"API Status: {status}")
        project_logs = db.collection(
            "projects", "olympiad-preparation", "components", "api", "logs"
        )
        await project_logs.add(
            {
                "timestamp": firestore.SERVER_TIMESTAMP,  # pyright: ignore[reportAttributeAccessIssue]
                "status": status,
            }
        )
