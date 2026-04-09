import asyncio
import random
from datetime import datetime, timedelta
from types import CoroutineType
from typing import Any

from redis.asyncio import Redis

from src.api.dependencies import get_firestore, get_redis
from src.core.constants import RedisKeys
from src.core.firebase import AsyncFirestore, initialize_firebase
from src.core.types import ServiceStatus
from src.schemas.projects_logs import ProjectLog

LOGS_MAX_OFFSET_DAYS = 30
LOGS_MIN_OFFSET_DAYS = 0

initialize_firebase()

db: AsyncFirestore = get_firestore()
redis: Redis = get_redis()


def get_random_status() -> ServiceStatus:
    value = random.randint(1, 100)
    if value > 98:
        return "outage"
    elif value > 90:
        return "degraded"
    return "operational"


async def generate_reports() -> None:
    projects_logs = db.collection("projects_logs")
    deleted_logs = await db.recursive_delete(projects_logs)
    print(f"Deleted logs: {deleted_logs}")

    projects_reports_coroutines: list[CoroutineType[Any, Any, tuple[Any, Any]]] = []

    for days_offset in range(LOGS_MAX_OFFSET_DAYS, LOGS_MIN_OFFSET_DAYS, -1):
        new_log_timestamp = datetime.now() - timedelta(days=days_offset - 1)
        api_status = get_random_status()
        site_status = get_random_status()
        static_assets_status = get_random_status()

        add_report_coroutine = projects_logs.add(
            ProjectLog(
                project_id="olympiad-preparation",
                project_name="Olympiad Preparation",
                timestamp=new_log_timestamp,  # pyright: ignore[reportAttributeAccessIssue]
                components={
                    "API": api_status,
                    "Site": site_status,
                    "Static assets": static_assets_status,
                },
            ).model_dump()
        )
        projects_reports_coroutines.append(add_report_coroutine)

        api_status = get_random_status()
        site_status = get_random_status()

        add_report_coroutine = projects_logs.add(
            ProjectLog(
                project_id="classic-word-game",
                project_name="Classic word game",
                timestamp=new_log_timestamp,  # pyright: ignore[reportAttributeAccessIssue]
                components={
                    "API": api_status,
                    "Site": site_status,
                },
            ).model_dump()
        )
        projects_reports_coroutines.append(add_report_coroutine)

    await asyncio.gather(*projects_reports_coroutines)
    print(f"Created projects logs: {len(projects_reports_coroutines)}")

    await redis.delete(RedisKeys.PROJECTS_REPORTS)
    print(f"Invalidated redis key: {RedisKeys.PROJECTS_REPORTS}")


asyncio.run(generate_reports())
