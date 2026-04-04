from httpx import Response


def is_successful_response(response: Response) -> bool:
    return response.is_success or response.is_redirect
