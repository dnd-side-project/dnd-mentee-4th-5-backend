from unittest import mock

import pytest
from jose import jwt

from auth.application.dtos import (
    GetTokenInputDto,
    GetTokenOutputDto,
    GetTokenDataInputDto,
    GetTokenDataOutputDto,
)
from auth.application.service import AuthApplicationService
from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import LoginOutputDto
from users.application.service import UserApplicationService


@pytest.fixture
def jwt_secret_key():
    return "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


@pytest.fixture
def jwt_algorithm():
    return "HS256"


@pytest.fixture
def auth_application_service():
    user_application_service_mock = mock.Mock(spec=UserApplicationService)
    user_application_service_mock.login.return_value = LoginOutputDto()

    AuthApplicationService(
        user_application_service=user_application_service_mock,
        jwt_secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        jwt_algorithm="HS256",
    )


def test_get_token_fail(jwt_secret_key, jwt_algorithm):
    user_application_service_mock = mock.Mock(spec=UserApplicationService)
    user_application_service_mock.login.return_value = FailedOutputDto.build_resource_not_found_error(
        "heumsi의 유저를 찾지 못했습니다."
    )
    auth_application_service = AuthApplicationService(
        user_application_service=user_application_service_mock,
        jwt_secret_key=jwt_secret_key,
        jwt_algorithm="jwt_algorithm",
    )

    input_dto = GetTokenInputDto(user_id="heumsi", password="1234")
    actual = auth_application_service.get_token(input_dto=input_dto)
    expected = FailedOutputDto.build_resource_error("heumsi의 유저를 찾지 못했습니다.")
    assert actual == expected


def test_get_token_success(jwt_secret_key, jwt_algorithm):
    user_application_service_mock = mock.Mock(spec=UserApplicationService)
    user_application_service_mock.login.return_value = LoginOutputDto()
    auth_application_service = AuthApplicationService(
        user_application_service=user_application_service_mock,
        jwt_secret_key=jwt_secret_key,
        jwt_algorithm=jwt_algorithm,
    )

    input_dto = GetTokenInputDto(user_id="heumsi", password="1234")
    actual = auth_application_service.get_token(input_dto=input_dto)
    expected = GetTokenOutputDto(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
    )
    assert actual == expected

    actual = jwt.decode(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I",
        key=jwt_secret_key,
        algorithms=jwt_algorithm,
    )
    expected = {"user_id": "heumsi"}
    assert actual == expected


def test_get_token_data_fail(jwt_secret_key, jwt_algorithm):
    auth_application_service = AuthApplicationService(
        user_application_service=mock.Mock(spec=UserApplicationService),
        jwt_secret_key=jwt_secret_key,
        jwt_algorithm=jwt_algorithm,
    )
    input_dto = GetTokenDataInputDto(access_token="wrong jwt token")

    actual = auth_application_service.get_token_data(input_dto)
    expected = FailedOutputDto.build_unauthorized_error(message="올바른 access-token이 아닙니다.")
    assert actual == expected


def test_get_token_data_success(jwt_secret_key, jwt_algorithm):
    auth_application_service = AuthApplicationService(
        user_application_service=mock.Mock(spec=UserApplicationService),
        jwt_secret_key=jwt_secret_key,
        jwt_algorithm=jwt_algorithm,
    )

    input_dto = GetTokenDataInputDto(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
    )
    actual = auth_application_service.get_token_data(input_dto)
    expected = GetTokenDataOutputDto(user_id="heumsi")
    assert actual == expected
