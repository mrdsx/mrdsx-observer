from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from core.firebase.client import initialize_firebase


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    initialize_firebase()
    yield
