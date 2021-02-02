from unittest.mock import Mock

import pytest
from jose import jwt

from auth.application.dtos import GetTokenInputDto, GetTokenOutputDto
from auth.application.service import AuthApplicationService
from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import LoginOutputDto
from users.application.service import UserApplicationService
from users.infra_structure.in_memory_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_application_service(user_repository):
    return UserApplicationService(user_repository)


@pytest.fixture
def auth_application_service(user_application_service):
    return AuthApplicationService(user_application_service=user_application_service)


def test_get_token(auth_application_service, user_application_service):
    input_dto = GetTokenInputDto(user_id="heumsi", password="1234")

    actual = auth_application_service.get_token(input_dto=input_dto)
    expected = FailedOutputDto.build_resource_error("heumsi의 유저를 찾지 못했습니다.")
    assert actual == expected

    user_application_service.login = Mock(return_value=LoginOutputDto())
    actual = auth_application_service.get_token(input_dto=input_dto)
    expected = GetTokenOutputDto(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
    )
    assert actual == expected

    actual = jwt.decode(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I",
        key=auth_application_service.SECRET_KEY,
        algorithms=auth_application_service.ALGORITHM,
    )
    expected = {"user_id": "heumsi"}
    assert actual == expected