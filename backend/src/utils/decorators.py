import functools
import json
from typing import Any

from pydantic import TypeAdapter, ValidationError
from redis.asyncio import Redis

from src.core.settings import get_settings

settings = get_settings()

redis = Redis(**settings.redis_settings)


def redis_cache(key: str, ttl: int, validation_model: Any):
    def wrapper(func):
        @functools.wraps(func)
        async def decorator(self, *args, **kwargs):
            try:
                cached_reports = await redis.get(name=key)
                if cached_reports is not None:
                    cached_reports = json.loads(cached_reports)
                    adapter = TypeAdapter(validation_model)

                    return adapter.validate_python(cached_reports)
            except (ValidationError, json.JSONDecodeError) as e:
                print(e)

            result = await func(self, *args, **kwargs)

            await redis.set(
                name=key,
                value=json.dumps(result, default=str),
                ex=ttl,
            )

            return result

        return decorator

    return wrapper
