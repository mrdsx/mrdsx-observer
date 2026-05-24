from functools import lru_cache

from redis.asyncio import Redis

from src.core.redis_cache import RedisCache


@lru_cache
def get_redis_cache(redis: Redis) -> RedisCache:
    return RedisCache(redis=redis)
