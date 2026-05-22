from collections.abc import AsyncGenerator

import pytest_asyncio
from psycopg import Connection
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.models import Base


@pytest_asyncio.fixture
async def session(postgresql: Connection) -> AsyncGenerator[AsyncSession, None]:
    user = postgresql.info.user
    host = postgresql.info.host
    port = postgresql.info.port
    dbname = postgresql.info.dbname

    connection_str = f"postgresql+asyncpg://{user}@{host}:{port}/{dbname}"
    engine = create_async_engine(connection_str, echo=False, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
