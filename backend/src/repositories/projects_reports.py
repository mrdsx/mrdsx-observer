from datetime import datetime

from google.cloud.firestore_v1 import And, DocumentSnapshot, FieldFilter
from google.cloud.firestore_v1.async_stream_generator import AsyncStreamGenerator

from src.core.constants import FirestoreKeys
from src.core.firebase.types import AsyncFirestore


class ProjectsReportsRepository:
    async def fetch_reports(
        self,
        start_date: datetime,
        end_date: datetime,
        db: AsyncFirestore,
    ) -> AsyncStreamGenerator[DocumentSnapshot]:
        reports_ref = db.collection(FirestoreKeys.PROJECTS_REPORTS).where(
            filter=And(
                [
                    FieldFilter("created_at", ">=", start_date),
                    FieldFilter("created_at", "<=", end_date),
                ]
            )
        )
        reports_stream = reports_ref.stream()

        return reports_stream
