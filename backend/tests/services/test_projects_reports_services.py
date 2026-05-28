import pytest
from httpx import AsyncClient

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
