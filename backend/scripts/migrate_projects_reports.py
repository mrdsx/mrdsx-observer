import asyncio

from pydantic import ValidationError

from src.api.dependencies import get_firestore
from src.core.constants import FirestoreKeys
from src.core.firebase import initialize_firebase
from src.schemas.projects_reports import (
    DailyProjectsReport_deprecated,
)


# TODO: remove migration script after migration is completed
async def migrate_projects_reports() -> None:
    initialize_firebase()
    db = get_firestore()
    batch = db.batch()

    collection = db.collection(FirestoreKeys.PROJECTS_REPORTS)
    reports_docs = await collection.get()

    for report_doc in reports_docs:
        try:
            daily_report = DailyProjectsReport_deprecated.model_validate(
                report_doc.to_dict()
            )
            for project_id, project_report in daily_report.projects.items():
                daily_report.projects[project_id] = project_report.services

            report_ref = db.collection(FirestoreKeys.PROJECTS_REPORTS).document(
                report_doc.id
            )
            batch.update(report_ref, daily_report.model_dump())
        except ValidationError as error:
            print(f"Skipping report update:\n{error}")

    await batch.commit()


asyncio.run(migrate_projects_reports())
