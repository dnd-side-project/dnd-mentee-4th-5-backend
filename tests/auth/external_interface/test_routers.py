from unittest import mock

import pytest

from auth.application.dtos import GetTokenOutputDto
from auth.application.service import AuthApplicationService
from auth.external_interface.json_dto import GetTokenJsonRequest
from shared_kernel.application.dtos import FailedOutputDto


@pytest.fixture(scope="function")
def auth_application_service_mock():
    return mock.Mock(spec=AuthApplicationService)


def test_get_token_success(auth_application_service_mock, app, client):
    auth_application_service_mock.get_token.return_value = GetTokenOutputDto(access_token="access token value")

    with app.container.auth_application_service.override(auth_application_service_mock):
        response = client.post(
            "/auth/token",
            json=GetTokenJsonRequest(user_id="heumsi", password="1234").dict(),
        )
    assert response.status_code == 200
    assert response.json() == {"access_token": "access token value"}


def test_get_token_fail(auth_application_service_mock, app, client):
    auth_application_service_mock.get_token.return_value = FailedOutputDto.build_resource_not_found_error(
        "heumsi의 유저를 찾지 못했습니다."
    )

    with app.container.auth_application_service.override(auth_application_service_mock):
        response = client.post(
            "/auth/token",
            json=GetTokenJsonRequest(user_id="heumsi", password="1234").dict(),
        )

    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "heumsi의 유저를 찾지 못했습니다.",
    }
