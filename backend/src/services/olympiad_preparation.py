import asyncio

from firebase_admin import firestore
from httpx import AsyncClient

from core.firebase.types import AsyncFirestore
from database.collections import get_component_logs_collection
from utils.response import get_project_status


async def capture_api(client: AsyncClient, db: AsyncFirestore) -> None:
    api_coro1 = client.get(
        "https://olympiad-preparation.vercel.app/api/math-problems?schoolGrade=1"
    )
    api_coro2 = client.get("https://olympiad-preparation.onrender.com/word-game")
    api_coro3 = client.get(
        "https://olympiad-preparation.vercel.app/api/matches?gridSize=3x4&schoolGrade=1&isFinalOlympiadStage=false"
    )
    responses = await asyncio.gather(api_coro1, api_coro2, api_coro3)
    status = get_project_status(*responses)

    print(f"API Status: {status}")
    project_logs = get_component_logs_collection(db, "olympiad-preparation", "api")
    await project_logs.add(
        {
            "timestamp": firestore.SERVER_TIMESTAMP,  # pyright: ignore[reportAttributeAccessIssue]
            "status": status,
        }
    )


async def capture_static_assets(client: AsyncClient, db: AsyncFirestore) -> None:
    response = await client.get("https://olympiad-preparation.vercel.app")
    status = get_project_status(response)

    print(f"Static assets status: {status}")
    project_logs = get_component_logs_collection(
        db, "olympiad-preparation", "static-assets"
    )
    await project_logs.add(
        {
            "timestamp": firestore.SERVER_TIMESTAMP,  # pyright: ignore[reportAttributeAccessIssue]
            "status": status,
        }
    )
