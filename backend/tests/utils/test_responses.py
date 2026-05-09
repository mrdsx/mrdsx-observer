from datetime import timedelta

from httpx import Response

from src.utils.responses import get_service_status, is_successful_response


class TestIsSuccessfulResponse:
    def test_is_successful_response_returns_success(self):
        response = Response(status_code=200)
        success = is_successful_response(response)
        assert success

    def test_is_successful_response_returns_success_with_4xx(self):
        response = Response(status_code=404)
        success = is_successful_response(response)
        assert success

    def test_is_successful_response_returns_not_success(self):
        response = Response(status_code=500)
        success = is_successful_response(response)
        assert not success


class TestGetServiceStatus:
    def test_get_service_status_returns_operational(self):
        responses = [
            Response(status_code=200),
            Response(status_code=200),
        ]

        for res in responses:
            res.elapsed = timedelta(seconds=0)

        status = get_service_status(*responses)
        assert status == "operational"

    def test_get_service_status_returns_degraded(self):
        responses = [
            Response(status_code=200),
            Response(status_code=200),
        ]

        for res in responses:
            res.elapsed = timedelta(seconds=20)

        status = get_service_status(*responses)
        assert status == "degraded"

    def test_get_service_status_returns_outage(self):
        responses = [
            Response(status_code=200),
            Response(status_code=500),
        ]

        for res in responses:
            res.elapsed = timedelta(seconds=0)

        status = get_service_status(*responses)
        assert status == "outage"
