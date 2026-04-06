import random
from datetime import timedelta

from httpx import AsyncClient, Response

from core.settings import get_settings

settings = get_settings()


async def send_request(client: AsyncClient, url: str) -> Response:
    if settings.app_env == "prod":
        return await client.get(url)

    status_code = 200
    # flaky behavior simulation
    if random.randint(1, 100) >= 99:
        status_code = 500

    # latency simulation
    response = Response(status_code=status_code)
    response.elapsed = timedelta(seconds=0)
    if random.randint(1, 10) >= 9:
        response.elapsed = timedelta(seconds=20)

    return response
