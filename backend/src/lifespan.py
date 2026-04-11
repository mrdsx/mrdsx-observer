from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.core.firebase.client import initialize_firebase
from src.core.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    print("Starting app with following settings:")
    print(f"Environment  - {settings.app_env}")
    print(f"Frontend URL - {settings.frontend_url}")
    print(f"Redis host   - {settings.redis_host}")
    print(f"Redis port   - {settings.redis_port}")

    initialize_firebase()
    yield
