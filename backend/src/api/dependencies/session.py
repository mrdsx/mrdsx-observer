from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        yield session
