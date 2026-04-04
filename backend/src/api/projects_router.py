from datetime import datetime, time, timedelta

from fastapi import APIRouter


router = APIRouter(prefix="/projects")


@router.get("/")
async def get_projects_status():
    now = datetime.now()
    start_date = (now - timedelta(days=89)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = datetime.combine(now.date(), time.max)


"""
{
    "projects": [
        {
            "id": "olympiad-preparation",
            "name": "Olympiad Preparation",
            "daily_data": [
                {
                    "date": (date.today() - timedelta(days=d)).isoformat(),
                    "uptime": None,
                }
                for d in range(90)
            ],
        }
    ],
}
"""


@router.get("/{project_id}")
async def get_project_status(project_id: str):
    return {"status": "ok"}
