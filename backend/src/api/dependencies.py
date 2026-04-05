from functools import lru_cache

from firebase_admin.firestore_async import client as create_async_firestore
from redis.asyncio import Redis

from core.firebase.types import AsyncFirestore
from core.settings import get_settings

settings = get_settings()


@lru_cache
def get_firestore() -> AsyncFirestore:
    return create_async_firestore()


@lru_cache
def get_redis() -> Redis:
    return Redis(**settings.redis_settings)
