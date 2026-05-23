from datetime import timedelta

from httpx import AsyncClient, Response
from starlette import status

from src.core.settings import get_settings

settings = get_settings()


async def send_request(url: str, http_client: AsyncClient) -> Response:
    if settings.app_env == "prod":
        return await http_client.get(url)

    response = Response(status_code=status.HTTP_200_OK)
    response.elapsed = timedelta(seconds=0)
    return response
