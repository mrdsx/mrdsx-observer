from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constants import project_names
from src.core.models.services_reports import (
    DailyServiceReportDTO,
    LatestServiceStatusDTO,
    ServiceReportsDTO,
)
from src.core.types import ServiceStatus
from src.repositories.projects_reports import ProjectsReportsRepository
from src.schemas.projects_reports_v2 import DailyProjectReport
from src.schemas.services_reports import ServicesReportsOut
from src.utils.datetime import isodate
from src.utils.math import truncate
from src.utils.projects_reports import (
    projects_reports_range,
    validate_daily_reports_v2,
)


class ServicesReportsService:
    async def get_services_reports(
        self,
        project_slug: str,
        projects_reports_repository: ProjectsReportsRepository,
        session: AsyncSession,
    ) -> ServicesReportsOut:
        start_date, end_date = projects_reports_range()
        raw_reports = await projects_reports_repository.fetch_reports_for_period(
            start_date=start_date, end_date=end_date, session=session
        )

        daily_reports = validate_daily_reports_v2(reports=raw_reports)
        normalized_reports = self._normalize_services_reports(
            project_slug=project_slug,
            daily_reports=daily_reports,
        )
        mapped_reports = self._map_services_reports(services_reports=normalized_reports)

        services_reports = ServicesReportsOut.model_validate(
            {
                "project_name": project_names.get(project_slug, project_slug),
                "services": mapped_reports,
            },
        )

        return services_reports

    def _normalize_services_reports(
        self,
        project_slug: str,
        daily_reports: list[DailyProjectReport],
    ) -> dict[str, ServiceReportsDTO]:
        services_reports: dict[str, ServiceReportsDTO] = {}
        latest_services_status: dict[str, LatestServiceStatusDTO] = {}

        for daily_report in daily_reports:
            if project_slug != daily_report.project_id:
                continue

            for service_name, service_report in daily_report.services_reports.items():
                # updating services reports (logs)
                existing_service_reports = services_reports.get(service_name)
                if existing_service_reports is None:
                    services_reports[service_name] = ServiceReportsDTO(daily_reports={})

                worst_status: ServiceStatus = "operational"
                if service_report.outages > 0:
                    worst_status = "outage"
                elif service_report.degraded > 0:
                    worst_status = "degraded"

                total_good_statuses = (
                    service_report.operational + service_report.degraded
                )
                total_statuses = total_good_statuses + service_report.outages
                uptime_percentage = (total_good_statuses / total_statuses) * 100

                services_reports[service_name].daily_reports[
                    isodate(daily_report.created_at)
                ] = DailyServiceReportDTO(
                    worst_status=worst_status,
                    uptime=truncate(uptime_percentage, 2),
                )

                # updating latest services status
                existing_latest_status = latest_services_status.get(service_name)
                if existing_latest_status is None:
                    latest_services_status[service_name] = LatestServiceStatusDTO(
                        created_at=daily_report.created_at,
                        current_status=service_report.current_status,
                        good_statuses=total_good_statuses,
                        total_statuses=total_statuses,
                    )
                else:
                    if existing_latest_status.created_at < daily_report.created_at:
                        latest_services_status[
                            service_name
                        ].created_at = daily_report.created_at
                        latest_services_status[
                            service_name
                        ].current_status = service_report.current_status

                    latest_services_status[
                        service_name
                    ].good_statuses += total_good_statuses
                    latest_services_status[
                        service_name
                    ].total_statuses += total_statuses

        if len(services_reports) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        for service_name, service_status in latest_services_status.items():
            uptime_percentage = (
                service_status.good_statuses / service_status.total_statuses
            ) * 100
            services_reports[service_name].uptime = truncate(uptime_percentage, 2)
            services_reports[
                service_name
            ].current_status = service_status.current_status

        return services_reports

    def _map_services_reports(
        self, services_reports: dict[str, ServiceReportsDTO]
    ) -> list[dict[str, Any]]:
        mapped_services_reports: list[dict[str, Any]] = []

        for service_name, service_report in services_reports.items():
            daily_service_reports = []

            for date, daily_report in service_report.daily_reports.items():
                daily_service_reports.append(
                    {
                        "date": date,
                        "worst_status": daily_report.worst_status,
                        "uptime": daily_report.uptime,
                    }
                )

            mapped_services_reports.append(
                {
                    "name": service_name,
                    "current_status": service_report.current_status,
                    "uptime": service_report.uptime,
                    "daily_reports": daily_service_reports,
                }
            )

        return mapped_services_reports
