from pathlib import Path

from redis.asyncio import Redis

from src.core.constants import TEST_LOCK_FILE
from src.core.settings import get_settings

settings = get_settings()


def get_redis() -> Redis:
    if Path(TEST_LOCK_FILE).is_file():
        settings.app_env = "test"
    return Redis(**settings.redis_settings)
