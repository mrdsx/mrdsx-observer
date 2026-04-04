import asyncio
from types import CoroutineType

from core.firebase.types import AsyncFirestore
from database.documents import get_project_component_doc, get_project_doc


async def migrate_database(db: AsyncFirestore) -> None:
    olympiad_coroutines = await get_olympiad_coroutines(db)

    await asyncio.gather(*olympiad_coroutines)


async def get_olympiad_coroutines(
    db: AsyncFirestore,
) -> list[CoroutineType]:
    project_doc = get_project_doc(db, "olympiad-preparation")
    project_coro = project_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "Olympiad Preparation"},
        merge=True,
    )

    static_assets_doc = get_project_component_doc(
        db, "olympiad-preparation", "static-assets"
    )
    static_assets_coro = static_assets_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "Static Assets"},
        merge=True,
    )

    api_doc = get_project_component_doc(db, "olympiad-preparation", "api")
    api_coro = api_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "API"},
        merge=True,
    )

    return [project_coro, static_assets_coro, api_coro]
