from redis.asyncio import Redis

from src.core.redis_cache import RedisCache


def get_redis_cache(redis: Redis) -> RedisCache:
    return RedisCache(redis=redis)
