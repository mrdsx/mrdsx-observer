from core.firebase.types import AsyncFirestore


async def migrate_database(db: AsyncFirestore) -> None:
    project_doc = db.document("projects", "olympiad-preparation")
    await project_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "Olympiad Preparation"},
        merge=True,
    )

    static_assets_doc = db.document(
        "projects", "olympiad-preparation", "components", "static-assets"
    )
    await static_assets_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "Static Assets"},
        merge=True,
    )

    api_doc = db.document("projects", "olympiad-preparation", "components", "api")
    await api_doc.set(  # pyright: ignore[reportUnknownMemberType]
        {"name": "API"},
        merge=True,
    )
