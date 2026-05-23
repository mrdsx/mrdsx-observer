import asyncio
from datetime import datetime
from typing import Any

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constants import project_names
from src.core.models.projects_reports import (
    DailyProjectReportDTO,
    ProjectReportDTO,
    ProjectStatusDTO,
)
from src.core.types import ServiceStatus
from src.repositories.projects_reports import ProjectsReportsRepository
from src.schemas.projects_reports import (
    DailyProjectReport,
    ProjectServiceReport,
    ProjectsReportsOut,
)
from src.utils.datetime import isodate
from src.utils.math import truncate
from src.utils.projects_reports import (
    projects_reports_range,
    validate_daily_reports,
    worst_status,
)
from src.utils.requests import send_request
from src.utils.responses import get_service_status


class ProjectsStateSnapshotter:
    async def capture_classic_word_game(
        self,
        http_client: AsyncClient,
    ) -> dict[str, ServiceStatus]:
        site_coro = send_request(
            "https://classic-word-game.vercel.app",
            http_client=http_client,
        )
        api_coro = send_request(
            "https://classic-word-game.onrender.com",
            http_client=http_client,
        )

        site_response, api_response = await asyncio.gather(site_coro, api_coro)

        site_status = get_service_status(site_response)
        api_status = get_service_status(api_response)

        return {
            "Site": site_status,
            "API": api_status,
        }

    async def capture_olympiad_preparation(
        self,
        http_client: AsyncClient,
    ) -> dict[str, ServiceStatus]:
        site_coro = send_request(
            "https://olympiad-preparation.vercel.app",
            http_client=http_client,
        )
        static_assets_coro = send_request(
            "https://res.cloudinary.com/dsf4g0owu/image/upload/w_160,c_limit/markelov-m-t_5_11_jcnm0o",
            http_client=http_client,
        )
        api_coro1 = send_request(
            "https://olympiad-preparation.vercel.app/api/math-problems?schoolGrade=2",
            http_client=http_client,
        )
        api_coro2 = send_request(
            "https://olympiad-preparation.onrender.com",
            http_client=http_client,
        )

        (
            site_response,
            static_assets_response,
            api_response1,
            api_response2,
        ) = await asyncio.gather(site_coro, static_assets_coro, api_coro1, api_coro2)

        site_status = get_service_status(site_response)
        static_assets_status = get_service_status(static_assets_response)
        api_status = get_service_status(api_response1, api_response2)

        return {
            "Site": site_status,
            "Static Assets": static_assets_status,
            "API": api_status,
        }

    async def capture_swift_tracker(
        self,
        http_client: AsyncClient,
    ) -> dict[str, ServiceStatus]:
        site_response = await send_request(
            "https://swift-tracker.net",
            http_client=http_client,
        )

        site_status = get_service_status(site_response)

        return {
            "Site": site_status,
        }


class ProjectsReportsService:
    async def get_projects_reports(
        self,
        projects_reports_repository: ProjectsReportsRepository,
        session: AsyncSession,
    ) -> ProjectsReportsOut:
        start_date, end_date = projects_reports_range()
        raw_reports = await projects_reports_repository.fetch_reports_for_period(
            start_date=start_date,
            end_date=end_date,
            session=session,
        )

        daily_reports = validate_daily_reports(raw_reports)
        normalized_reports, latest_projects_status = self._normalize_projects_reports(
            daily_reports=daily_reports
        )
        projects_status = self._compute_projects_status_and_uptime(
            projects_reports=normalized_reports,
            latest_projects_status=latest_projects_status,
        )
        mapped_projects_reports = self._map_projects_reports(
            projects_reports=projects_status
        )
        projects_reports = ProjectsReportsOut.model_validate(
            {"projects": mapped_projects_reports}
        )

        return projects_reports

    def _normalize_projects_reports(
        self,
        daily_reports: list[DailyProjectReport],
    ) -> tuple[dict[str, ProjectReportDTO], dict[str, Any]]:
        projects_reports: dict[str, ProjectReportDTO] = {}
        latest_projects_status: dict[str, Any] = {}

        for daily_report in daily_reports:
            project_id = daily_report.project_id
            existing_project_reports = projects_reports.get(project_id)
            if existing_project_reports is None:
                projects_reports[project_id] = ProjectReportDTO(
                    name=project_names.get(project_id, project_id),
                    daily_reports={},
                )

            status_data = self._compute_project_status(daily_report.services_reports)

            projects_reports[project_id].daily_reports[
                isodate(daily_report.created_at)
            ] = DailyProjectReportDTO(
                worst_status=status_data.worst_status,
                uptime=truncate(status_data.uptime_percentage, 2),
            )

            self._update_latest_project_status(
                latest_projects_status=latest_projects_status,
                created_at=daily_report.created_at,
                project_id=project_id,
                services_status=status_data.services_status,
                good_statuses=status_data.good_statuses,
                outages=status_data.outages,
            )

        return projects_reports, latest_projects_status

    def _update_latest_project_status(
        self,
        latest_projects_status: dict[str, Any],
        created_at: datetime,
        project_id: str,
        services_status: set[ServiceStatus],
        good_statuses: int,
        outages: int,
    ) -> None:
        """Modifies `latest_projects_status` in-place."""

        project_status = latest_projects_status.get(project_id)
        if project_status is None:
            latest_projects_status[project_id] = {
                "latest_report": created_at,
                "good_statuses": 0,
                "outages": 0,
            }

        if created_at >= latest_projects_status[project_id]["latest_report"]:
            latest_projects_status[project_id]["latest_report"] = created_at
            latest_projects_status[project_id]["current_status"] = worst_status(
                *services_status
            )
        latest_projects_status[project_id]["good_statuses"] += good_statuses
        latest_projects_status[project_id]["outages"] += outages

    def _compute_project_status(
        self,
        project_services: dict[str, ProjectServiceReport],
    ) -> ProjectStatusDTO:
        total_good_statuses = 0
        total_outages = 0
        worst_status: ServiceStatus = "operational"
        services_status: set[ServiceStatus] = set()

        for _, service_report in project_services.items():
            total_good_statuses += service_report.operational + service_report.degraded
            total_outages += service_report.outages

            services_status.add(service_report.current_status)
            if worst_status != "outage" and service_report.outages > 0:
                worst_status = "outage"
            elif worst_status == "operational" and service_report.degraded > 0:
                worst_status = "degraded"

        total_statuses = total_good_statuses + total_outages
        uptime_percentage = (total_good_statuses / total_statuses) * 100

        return ProjectStatusDTO(
            uptime_percentage=uptime_percentage,
            worst_status=worst_status,
            services_status=services_status,
            good_statuses=total_good_statuses,
            outages=total_outages,
        )

    def _compute_projects_status_and_uptime(
        self,
        projects_reports: dict[str, ProjectReportDTO],
        latest_projects_status: dict[str, Any],
    ) -> dict[str, ProjectReportDTO]:
        """Computes current status and uptime and attaches them as attributes to returned object."""

        for project_id, _ in projects_reports.items():
            projects_reports[project_id].current_status = latest_projects_status[
                project_id
            ]["current_status"]

            total_good_statuses = latest_projects_status[project_id]["good_statuses"]
            total_outages = latest_projects_status[project_id]["outages"]
            total_statuses = total_good_statuses + total_outages
            uptime_percentage = (total_good_statuses / total_statuses) * 100

            projects_reports[project_id].uptime = truncate(uptime_percentage, 2)

        return projects_reports

    def _map_projects_reports(
        self,
        projects_reports: dict[str, ProjectReportDTO],
    ) -> list[dict[str, Any]]:
        """Maps projects reports by flatting the dictionaries to lists.

        For example, the object
        `{"2026-01-01": {...}, "2026-01-02": {...}}`
        will be mapped to:
        `[{"date": "2026-01-01", ...}, {"date": "2026-01-02", ...}]`
        """

        mapped_reports: list[dict[str, Any]] = []

        for project_id, project_report in projects_reports.items():
            mapped_daily_reports: list[dict[str, Any]] = []

            for date, daily_report in project_report.daily_reports.items():
                mapped_daily_reports.append(
                    {
                        "date": date,
                        "worst_status": daily_report.worst_status,
                        "uptime": daily_report.uptime,
                    }
                )

            mapped_reports.append(
                {
                    "id": project_id,
                    "name": project_report.name,
                    "daily_reports": mapped_daily_reports,
                    "current_status": project_report.current_status,
                    "uptime": project_report.uptime,
                }
            )

        return mapped_reports


class DailyProjectReportsUpdater:
    async def update_daily_reports(
        self,
        projects_reports_repository: ProjectsReportsRepository,
        snapshotter: ProjectsStateSnapshotter,
        http_client: AsyncClient,
        session: AsyncSession,
    ) -> None:
        projects_status = await self._get_projects_status(
            snapshotter=snapshotter,
            http_client=http_client,
        )

        current_date = datetime.now()
        raw_reports = await projects_reports_repository.fetch_reports_by_day(
            current_date=current_date,
            session=session,
        )
        daily_reports = validate_daily_reports(raw_reports)

        for project_id, services_status in projects_status:
            services_reports: dict[str, ProjectServiceReport] | None = None

            for daily_report in daily_reports:
                if daily_report.project_id == project_id:
                    services_reports = daily_report.services_reports

            if services_reports is None:
                services_reports = self._derive_services_reports(
                    services_status=services_status,
                )
                await projects_reports_repository.insert_report(
                    project_id=project_id,
                    current_date=current_date,
                    services_reports=services_reports,
                    session=session,
                )
            else:
                self._update_project_report(
                    services_reports=services_reports,
                    services_status=services_status,
                )
                await projects_reports_repository.update_report(
                    project_id=project_id,
                    current_date=current_date,
                    services_reports=services_reports,
                    session=session,
                )

    async def _get_projects_status(
        self,
        snapshotter: ProjectsStateSnapshotter,
        http_client: AsyncClient,
    ) -> list[tuple[str, dict[str, ServiceStatus]]]:
        async with asyncio.TaskGroup() as task_group:
            task1 = task_group.create_task(
                snapshotter.capture_olympiad_preparation(http_client=http_client)
            )
            task2 = task_group.create_task(
                snapshotter.capture_classic_word_game(http_client=http_client)
            )
            task3 = task_group.create_task(
                snapshotter.capture_swift_tracker(http_client=http_client)
            )

        projects_status: list[tuple[str, dict[str, ServiceStatus]]] = [
            ("olympiad-preparation", task1.result()),
            ("classic-word-game", task2.result()),
            ("swift-tracker", task3.result()),
        ]

        return projects_status

    def _derive_services_reports(
        self,
        services_status: dict[str, ServiceStatus],
    ) -> dict[str, ProjectServiceReport]:
        services_reports: dict[str, ProjectServiceReport] = {}

        for service_name, service_status in services_status.items():
            self._insert_project_service_report(
                services_reports=services_reports,
                service_name=service_name,
                service_status=service_status,
            )

        return services_reports

    def _update_project_report(
        self,
        services_reports: dict[str, ProjectServiceReport],
        services_status: dict[str, ServiceStatus],
    ) -> None:
        for service_name, service_status in services_status.items():
            service_details = services_reports.get(service_name)
            if service_details is None:
                self._insert_project_service_report(
                    services_reports=services_reports,
                    service_name=service_name,
                    service_status=service_status,
                )
            else:
                services_reports[service_name].current_status = service_status
                if service_status == "operational":
                    services_reports[service_name].operational += 1
                elif service_status == "degraded":
                    services_reports[service_name].degraded += 1
                elif service_status == "outage":
                    services_reports[service_name].outages += 1

    def _insert_project_service_report(
        self,
        services_reports: dict[str, ProjectServiceReport],
        service_name: str,
        service_status: ServiceStatus,
    ) -> None:
        operational = 1 if service_status == "operational" else 0
        degraded = 1 if service_status == "degraded" else 0
        outages = 1 if service_status == "outage" else 0

        services_reports[service_name] = ProjectServiceReport(
            current_status=service_status,
            operational=operational,
            degraded=degraded,
            outages=outages,
        )
