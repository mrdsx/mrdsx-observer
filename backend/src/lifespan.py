from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.core.settings import get_settings
from src.models import dispose_db, initialize_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    if settings.app_env == "dev":
        print("Starting app with following settings:")
        print(f"Environment   - {settings.app_env}")
        print(f"Postgres host - {settings.db_host}")
        print(f"Postgres port - {settings.db_port}")

    await initialize_db()
    yield
    await dispose_db()
