import asyncio
from types import CoroutineType

from core.firebase.types import AsyncFirestore


async def migrate_database(db: AsyncFirestore) -> None:
    olympiad_coroutines = await get_olympiad_coroutines(db)

    await asyncio.gather(*olympiad_coroutines)


async def get_olympiad_coroutines(
    db: AsyncFirestore,
) -> list[CoroutineType]:
    project_doc = db.document("projects", "olympiad-preparation")
    coroutine1 = project_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "Olympiad Preparation"},
        merge=True,
    )

    static_assets_doc = db.document(
        "projects", "olympiad-preparation", "components", "static-assets"
    )
    coroutine2 = static_assets_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "Static Assets"},
        merge=True,
    )

    api_doc = db.document("projects", "olympiad-preparation", "components", "api")
    coroutine3 = api_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "API"},
        merge=True,
    )

    return [coroutine1, coroutine2, coroutine3]
