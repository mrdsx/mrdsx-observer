from datetime import datetime

import pytest
import pytest_asyncio
from pydantic import ValidationError
from redis.asyncio import Redis

from src.api.dependencies.redis_cache import get_redis_cache
from src.core.settings import get_settings

settings = get_settings()


@pytest_asyncio.fixture
async def mock_class(redis: Redis):
    redis_cache = get_redis_cache(redis=redis)

    class MockClass:
        @redis_cache.ttl_cache(
            key="current_date",
            ttl=10,
            validation_model=str,
        )
        async def current_date(self) -> str:
            return datetime.now().isoformat()

        @redis_cache.ttl_cache(
            key="wrong_type",
            ttl=10,
            validation_model=int,
        )
        async def wrong_type(self) -> str:
            return "wrong type"

    return MockClass()


@pytest.mark.asyncio
async def test_ttl_cache_without_refresh(mock_class):
    first_date = await mock_class.current_date()
    second_date = await mock_class.current_date()
    assert first_date == second_date


@pytest.mark.asyncio
async def test_ttl_cache_with_refresh(mock_class):
    """
    If we set 'force_refresh' to True
    new date will be generated on each 'current_date' call
    so multiple dates must be unique.
    """

    first_date = await mock_class.current_date(force_refresh=True)
    second_date = await mock_class.current_date(force_refresh=True)
    assert first_date != second_date


@pytest.mark.asyncio
async def test_ttl_cache_raises_validation_error(mock_class):
    with pytest.raises(ValidationError):
        await mock_class.wrong_type()
