from httpx import Response

from src.core.constants import MIN_RESPONSE_SECONDS
from src.core.types import ServiceStatus


def is_successful_response(response: Response) -> bool:
    return response.is_success or response.is_redirect


def get_service_status(*responses: Response) -> ServiceStatus:
    success_list = [is_successful_response(res) for res in responses]
    elapsed_seconds_list = [res.elapsed.seconds for res in responses]

    if False in success_list:
        return "outage"
    elif any(time >= MIN_RESPONSE_SECONDS for time in elapsed_seconds_list):
        return "degraded"
    return "operational"
