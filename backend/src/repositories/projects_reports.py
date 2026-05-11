from datetime import datetime
from typing import Any

from google.cloud.firestore_v1 import And, FieldFilter

from src.core.constants import FirestoreKeys
from src.core.firebase.types import AsyncFirestore


class ProjectsReportsRepository:
    async def fetch_reports(
        self,
        start_date: datetime,
        end_date: datetime,
        db: AsyncFirestore,
    ) -> list[dict[str, Any]]:
        reports_ref = db.collection(FirestoreKeys.PROJECTS_REPORTS).where(
            filter=And(
                [
                    FieldFilter("created_at", ">=", start_date),
                    FieldFilter("created_at", "<=", end_date),
                ]
            )
        )
        reports_stream = reports_ref.stream()

        result: list[dict[str, Any]] = []
        async for report in reports_stream:
            report_dict = report.to_dict()
            if report_dict is not None:
                result.append(report_dict)

        return result

    async def delete_old_reports(
        self,
        cutoff_date: datetime,
        db: AsyncFirestore,
    ) -> None:
        reports_ref = db.collection(FirestoreKeys.PROJECTS_REPORTS).where(
            filter=FieldFilter("created_at", "<", cutoff_date)
        )
        reports_stream = reports_ref.stream()

        batch = db.batch()
        async for report in reports_stream:
            batch.delete(report.reference)
        await batch.commit()
