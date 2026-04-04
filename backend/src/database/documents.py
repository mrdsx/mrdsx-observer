from core.firebase.types import AsyncDocumentReference, AsyncFirestore


def get_project_doc(
    db: AsyncFirestore,
    project_name: str,
) -> AsyncDocumentReference:
    return db.document("projects", project_name)


def get_project_component_doc(
    db: AsyncFirestore,
    project_name: str,
    component_name: str,
) -> AsyncDocumentReference:
    return db.document("projects", project_name, "components", component_name)
