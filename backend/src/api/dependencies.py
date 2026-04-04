from functools import lru_cache

from firebase_admin.firestore_async import client as create_async_firestore

from core.firebase.types import AsyncFirestore


@lru_cache
def get_firestore() -> AsyncFirestore:
    return create_async_firestore()
