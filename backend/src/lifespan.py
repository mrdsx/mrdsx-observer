from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from api.dependencies import get_firestore
from core.firebase.client import initialize_firebase
from database.migrations import migrate_database


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    initialize_firebase()

    db = get_firestore()
    await migrate_database(db)

    yield
