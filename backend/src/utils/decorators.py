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
            type_adapter = TypeAdapter(validation_model)

            try:
                cached_data = await redis.get(name=key)
                if cached_data is not None:
                    cached_data = json.loads(cached_data)
                    type_adapter.validate_python(cached_data)

                    return cached_data
            except (ValidationError, json.JSONDecodeError) as e:
                print(e)

            result = await func(self, *args, **kwargs)
            type_adapter.validate_python(result)

            await redis.set(
                name=key,
                value=json.dumps(result, default=str),
                ex=ttl,
            )

            return result

        return decorator

    return wrapper
