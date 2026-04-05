import asyncio

from firebase_admin import firestore
from httpx import AsyncClient

from core.firebase.types import AsyncFirestore
from schemas.projects_logs import ProjectLog
from utils.response import get_service_status


async def capture_olympiad_preparation(client: AsyncClient, db: AsyncFirestore) -> None:
    api_coro1 = client.get(
        "https://olympiad-preparation.vercel.app/api/math-problems?schoolGrade=1"
    )
    api_coro2 = client.get("https://olympiad-preparation.onrender.com/word-game")
    api_coro3 = client.get(
        "https://olympiad-preparation.vercel.app/api/matches?gridSize=3x4&schoolGrade=1&isFinalOlympiadStage=false"
    )
    static_assets_coro = client.get("https://olympiad-preparation.vercel.app")
    *api_responses, static_assets_response = await asyncio.gather(
        api_coro1, api_coro2, api_coro3, static_assets_coro
    )

    api_status = get_service_status(*api_responses)
    static_assets_status = get_service_status(static_assets_response)

    print(f"API status: {api_status}")
    print(f"Static assets status: {static_assets_status}")

    projects_logs = db.collection("projects_logs")
    await projects_logs.add(
        ProjectLog(
            project_id="olympiad-preparation",
            project_name="Olympiad Preparation",
            timestamp=firestore.SERVER_TIMESTAMP,  # pyright: ignore[reportAttributeAccessIssue]
            components={
                "API": api_status,
                "Static assets": static_assets_status,
            },
        ).model_dump()
    )
