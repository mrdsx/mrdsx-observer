import pytest
from httpx import AsyncClient

from src.api.dependencies import get_projects_reports_service
from src.core.models.projects_reports import DailyProjectReportDTO, ProjectReportDTO
from src.services.projects_reports import ProjectsStateSnapshotter


@pytest.mark.asyncio
class TestProjectsStateSnapshotter:
    snapshotter = ProjectsStateSnapshotter()

    async def test_capture_classic_word_game(self, http_client: AsyncClient):
        status = await self.snapshotter.capture_classic_word_game(
            http_client=http_client
        )
        assert status == {
            "Site": "operational",
            "API": "operational",
        }

    async def test_capture_olympiad_preparation(self, http_client: AsyncClient):
        status = await self.snapshotter.capture_olympiad_preparation(
            http_client=http_client
        )
        assert status == {
            "Site": "operational",
            "Static Assets": "operational",
            "API": "operational",
        }

    async def test_capture_swift_tracker(self, http_client: AsyncClient):
        status = await self.snapshotter.capture_swift_tracker(http_client=http_client)
        assert status == {
            "Site": "operational",
        }


class TestProjectsReportsService:
    projects_reports_service = get_projects_reports_service()

    def test_map_projects_reports(self):
        projects_reports = {
            "project1": ProjectReportDTO(
                name="Project 1",
                daily_reports={
                    "2027-01-01": DailyProjectReportDTO(
                        worst_status="operational",
                        uptime=100,
                    )
                },
                current_status="operational",
                uptime=100,
            ),
            "project2": ProjectReportDTO(
                name="Project 2",
                daily_reports={
                    "2027-01-01": DailyProjectReportDTO(
                        worst_status="degraded",
                        uptime=100,
                    )
                },
                current_status="degraded",
                uptime=100,
            ),
            "project3": ProjectReportDTO(
                name="Project 3",
                daily_reports={
                    "2027-01-01": DailyProjectReportDTO(
                        worst_status="operational",
                        uptime=100,
                    ),
                    "2027-01-02": DailyProjectReportDTO(
                        worst_status="outage",
                        uptime=0,
                    ),
                },
                current_status="outage",
                uptime=50,
            ),
        }
        mapped_projects_reports = self.projects_reports_service._map_projects_reports(
            projects_reports=projects_reports
        )
        assert mapped_projects_reports == [
            {
                "id": "project1",
                "name": "Project 1",
                "daily_reports": [
                    {
                        "date": "2027-01-01",
                        "worst_status": "operational",
                        "uptime": 100,
                    },
                ],
                "current_status": "operational",
                "uptime": 100,
            },
            {
                "id": "project2",
                "name": "Project 2",
                "daily_reports": [
                    {
                        "date": "2027-01-01",
                        "worst_status": "degraded",
                        "uptime": 100,
                    },
                ],
                "current_status": "degraded",
                "uptime": 100,
            },
            {
                "id": "project3",
                "name": "Project 3",
                "daily_reports": [
                    {
                        "date": "2027-01-01",
                        "worst_status": "operational",
                        "uptime": 100,
                    },
                    {
                        "date": "2027-01-02",
                        "worst_status": "outage",
                        "uptime": 0,
                    },
                ],
                "current_status": "outage",
                "uptime": 50,
            },
        ]
