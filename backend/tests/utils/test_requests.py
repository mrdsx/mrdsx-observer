import httpx
import pytest
from starlette import status

from src.utils.requests import send_request


@pytest.mark.asyncio
async def test_send_request():
    async with httpx.AsyncClient() as http_client:
        response = await send_request("https://example.com", http_client=http_client)
        assert response.status_code == status.HTTP_200_OK
