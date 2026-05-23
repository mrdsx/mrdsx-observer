from datetime import datetime
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constants import CACHE_TTL_SECONDS, RedisKeys
from src.models.projects_reports import DB_DailyProjectReport
from src.schemas.projects_reports import DailyProjectReport, ProjectServiceReport
from src.utils.datetime import isodate
from src.utils.db import deserialize_rows
from src.utils.decorators import redis_cache


class ProjectsReportsRepository:
    @redis_cache(
        key=RedisKeys.PROJECTS_REPORTS,
        ttl=CACHE_TTL_SECONDS,
        validation_model=list[DailyProjectReport],
    )
    async def fetch_reports_for_period(
        self,
        start_date: datetime,
        end_date: datetime,
        session: AsyncSession,
    ) -> list[dict[str, Any]]:
        result = await session.execute(
            select(DB_DailyProjectReport).where(
                DB_DailyProjectReport.created_at.between(start_date, end_date)
            )
        )

        return deserialize_rows(result)

    async def fetch_reports_by_day(
        self,
        current_date: datetime,
        session: AsyncSession,
    ) -> list[dict[str, Any]]:
        result = await session.execute(
            select(DB_DailyProjectReport).where(
                DB_DailyProjectReport.date_str == isodate(current_date)
            )
        )

        return deserialize_rows(result)

    async def insert_report(
        self,
        project_id: str,
        current_date: datetime,
        services_reports: dict[str, ProjectServiceReport],
        session: AsyncSession,
    ) -> None:
        session.add(
            DB_DailyProjectReport(
                project_id=project_id,
                date_str=isodate(current_date),
                created_at=current_date,
                services_reports={
                    service_name: service_report.model_dump()
                    for service_name, service_report in services_reports.items()
                },
            )
        )
        await session.commit()

    async def update_report(
        self,
        project_id: str,
        current_date: datetime,
        services_reports: dict[str, ProjectServiceReport],
        session: AsyncSession,
    ) -> None:
        await session.execute(
            update(DB_DailyProjectReport)
            .where(
                DB_DailyProjectReport.project_id == project_id,
                DB_DailyProjectReport.date_str == isodate(current_date),
            )
            .values(
                services_reports={
                    service_name: service_report.model_dump()
                    for service_name, service_report in services_reports.items()
                }
            )
        )
        await session.commit()

    async def delete_old_reports(
        self,
        cutoff_date: datetime,
        session: AsyncSession,
    ) -> None:
        await session.execute(
            delete(DB_DailyProjectReport).where(
                DB_DailyProjectReport.created_at < cutoff_date
            )
        )
        await session.commit()
