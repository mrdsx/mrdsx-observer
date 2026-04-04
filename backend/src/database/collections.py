from core.firebase.types import AsyncCollectionReference, AsyncFirestore


def get_component_logs_collection(
    db: AsyncFirestore,
    project_name: str,
    component_name: str,
) -> AsyncCollectionReference:
    return db.collection(
        "projects",
        project_name,
        "components",
        component_name,
        "logs",
    )
