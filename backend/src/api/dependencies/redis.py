from functools import lru_cache

from redis.asyncio import Redis

from src.core.settings import get_settings

settings = get_settings()


@lru_cache
def get_redis() -> Redis:
    return Redis(**settings.redis_settings)
