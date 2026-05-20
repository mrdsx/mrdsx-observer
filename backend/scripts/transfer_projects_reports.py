import asyncio
from datetime import datetime

from sqlalchemy import delete

from src.api.dependencies import get_firestore
from src.api.dependencies.session import get_session
from src.core.constants import FirestoreKeys
from src.core.firebase import initialize_firebase
from src.models import initialize_db
from src.models.projects_reports import DB_DailyProjectReport
from src.utils.datetime import isodate
from src.utils.projects_reports import validate_daily_reports


async def main() -> None:
    await initialize_db()
    initialize_firebase()

    # TODO: remove get_firestore and deprecated functions after migration to postgres
    firestore = get_firestore()
    raw_reports = await firestore.collection(FirestoreKeys.PROJECTS_REPORTS).get()
    raw_reports = [report.to_dict() for report in raw_reports]
    daily_reports = validate_daily_reports(raw_reports)

    async for session in get_session():
        await session.execute(delete(DB_DailyProjectReport))
        print("Cleared projects reports table")

        for daily_report in daily_reports:
            date_str = isodate(daily_report.created_at)
            created_at = datetime.fromisoformat(
                daily_report.created_at.isoformat()
            ).replace(tzinfo=None)

            for project_id, services_reports in daily_report.projects.items():
                mapped_services_reports = {
                    service_id: service_report.model_dump()
                    for service_id, service_report in services_reports.items()
                }

                session.add(
                    DB_DailyProjectReport(
                        project_id=project_id,
                        date_str=date_str,
                        created_at=created_at,
                        services_reports=mapped_services_reports,
                    )
                )

            print(f"Added batch write for date {date_str}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
