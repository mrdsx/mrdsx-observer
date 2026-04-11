from httpx import Response

from src.core.constants import MAX_RESPONSE_TIME_SECONDS
from src.core.types import ServiceStatus


def is_successful_response(response: Response) -> bool:
    return not response.is_server_error


def get_service_status(*responses: Response) -> ServiceStatus:
    success_list = [is_successful_response(res) for res in responses]
    elapsed_seconds_list = [res.elapsed.seconds for res in responses]

    if False in success_list:
        return "outage"
    elif any(time >= MAX_RESPONSE_TIME_SECONDS for time in elapsed_seconds_list):
        return "degraded"
    return "operational"
