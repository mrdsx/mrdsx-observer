import asyncio

from firebase_admin import firestore
from httpx import AsyncClient

from core.firebase.types import AsyncFirestore
from schemas.projects_logs import ProjectLog
from utils.requests import send_request
from utils.responses import get_service_status


async def capture_classic_word_game(client: AsyncClient, db: AsyncFirestore) -> None:
    api_coro = send_request(client, "https://classic-word-game.onrender.com")
    site_coro = send_request(client, "https://classic-word-game.vercel.app")

    api_response, site_response = await asyncio.gather(api_coro, site_coro)

    api_status = get_service_status(api_response)
    site_status = get_service_status(site_response)

    projects_logs = db.collection("projects_logs")
    await projects_logs.add(
        ProjectLog(
            project_id="classic-word-game",
            project_name="Classic word game",
            timestamp=firestore.SERVER_TIMESTAMP,  # pyright: ignore[reportAttributeAccessIssue]
            components={
                "API": api_status,
                "Site": site_status,
            },
        ).model_dump()
    )


async def capture_olympiad_preparation(client: AsyncClient, db: AsyncFirestore) -> None:
    api_coro1 = send_request(
        client,
        "https://olympiad-preparation.vercel.app/api/math-problems?schoolGrade=1",
    )
    api_coro2 = send_request(
        client,
        "https://olympiad-preparation.onrender.com/word-game",
    )
    site_coro = send_request(client, "https://olympiad-preparation.vercel.app")
    storage_coro = send_request(
        client,
        "https://res.cloudinary.com/dsf4g0owu/image/upload/w_160,c_limit/ruslo_fhbyle",
    )

    *api_responses, site_response, storage_response = await asyncio.gather(
        api_coro1, api_coro2, site_coro, storage_coro
    )

    api_status = get_service_status(*api_responses)
    static_assets_status = get_service_status(site_response, storage_response)

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
