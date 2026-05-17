import asyncio

from pydantic import ValidationError

from src.api.dependencies import get_firestore
from src.api.dependencies.redis import get_redis
from src.core.constants import FirestoreKeys, RedisKeys
from src.core.firebase import initialize_firebase
from src.schemas.projects_reports import DailyProjectsReport


async def delete_mrdsx_observer_reports() -> None:
    initialize_firebase()
    db = get_firestore()
    redis = get_redis()
    batch = db.batch()

    reports_ref = db.collection(FirestoreKeys.PROJECTS_REPORTS)
    reports = reports_ref.stream()

    async for report_snapshot in reports:
        raw_report = report_snapshot.to_dict()
        try:
            report = DailyProjectsReport.model_validate(raw_report)
            report.projects.pop("mrdsx-observer", None)
            batch.update(report_snapshot.reference, report.model_dump())

            print(f"Added batch update for document with doc_id: {report_snapshot.id}")
        except ValidationError as e:
            print(f"Validation failed for doc_id '{report_snapshot.id}': {e}")

    await batch.commit()
    await redis.delete(RedisKeys.PROJECTS_REPORTS)
    print(f"Invalidated cache for {RedisKeys.PROJECTS_REPORTS}")


if __name__ == "__main__":
    asyncio.run(delete_mrdsx_observer_reports())
