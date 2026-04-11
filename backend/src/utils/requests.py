import random
from datetime import timedelta

from httpx import AsyncClient, Response

from src.core.settings import get_settings

settings = get_settings()


async def send_request(url: str, http_client: AsyncClient) -> Response:
    if settings.app_env == "prod":
        return await http_client.get(url)

    status_code = 200
    # flaky behavior simulation
    if random.randint(1, 1000) >= 998:
        status_code = 500

    # latency simulation
    response = Response(status_code=status_code)
    response.elapsed = timedelta(seconds=0)
    if random.randint(1, 100) >= 98:
        response.elapsed = timedelta(seconds=20)

    return response
