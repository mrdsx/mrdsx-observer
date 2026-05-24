import functools
import json
from typing import Any

from pydantic import TypeAdapter, ValidationError
from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def ttl_cache(self, key: str, ttl: int, validation_model: Any):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(
                cls,
                force_refresh: bool = False,
                *args,
                **kwargs,
            ):
                type_adapter = TypeAdapter(validation_model)

                if not force_refresh:
                    try:
                        cached_data = await self._redis.get(name=key)
                        if cached_data is not None:
                            cached_data = json.loads(cached_data)
                            type_adapter.validate_python(cached_data)

                            return cached_data
                    except (ValidationError, json.JSONDecodeError) as e:
                        print(e)

                result = await func(self, *args, **kwargs)
                type_adapter.validate_python(result)

                await self._redis.set(
                    name=key,
                    value=json.dumps(result, default=str),
                    ex=ttl,
                )

                return result

            return wrapper

        return decorator
