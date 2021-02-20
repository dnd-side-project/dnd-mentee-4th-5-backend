from unittest import mock

import pytest

from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from users.application.dtos import (
    CreateUserInputDto,
    CreateUserOutputDto,
    DeleteUserInputDto,
    FindUserInputDto,
    FindUserOutputDto,
    LoginInputDto,
    LoginOutputDto,
    UpdateUserInputDto,
    UpdateUserOutputDto,
    DeleteUserOutputDto,
)
from users.application.service import UserApplicationService
from users.domain.entities import User
from users.domain.repository import UserRepository
from shared_kernel.domain.value_objects import UserId, UserName

user_data = [("heumsi", "heumsi", "1234")]


@pytest.fixture(scope="function")
def user_repository_mock():
    return mock.Mock(spec=UserRepository)


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_find_user_success(user_repository_mock, user_id, user_name, password):
    user_repository_mock.find_by_user_id.return_value = User(
        id=UserId(value=user_id), name=UserName(value=user_name), password=password
    )
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = FindUserInputDto(user_id=user_id)
    actual = user_application_service.find_user(input_dto)
    expected = FindUserOutputDto(user_id=user_id, user_name=user_name, description="", image_url="")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_find_user_fail(user_repository_mock, user_id, user_name, password):
    user_repository_mock.find_by_user_id.side_effect = ResourceNotFoundError()
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = FindUserInputDto(user_id="not exist user")
    actual = user_application_service.find_user(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_create_user_success(user_repository_mock, user_id, user_name, password):
    user_repository_mock.add.return_value = None
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = CreateUserInputDto(user_id=user_id, user_name=user_name, password=password)
    actual = user_application_service.create_user(input_dto)
    expected = CreateUserOutputDto(user_id=user_id, user_name=user_name, description="", image_url="")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_create_user_fail(user_repository_mock, user_id, user_name, password):
    user_repository_mock.add.side_effect = ResourceAlreadyExistError()
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = CreateUserInputDto(user_id=user_id, user_name=user_name, password=password)
    actual = user_application_service.create_user(input_dto)
    expected = FailedOutputDto(type="Resource Conflict Error", message="")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_update_user_success(user_repository_mock, user_id, user_name, password):
    user_repository_mock.update.return_value = None
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = UpdateUserInputDto(user_id=user_id, user_name="siheum", description="hi, I'm siheum!", password="4321")
    actual = user_application_service.update_user(input_dto)
    expected = UpdateUserOutputDto()
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_update_user_fail(user_repository_mock, user_id, user_name, password):
    user_repository_mock.update.side_effect = ResourceNotFoundError()
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = UpdateUserInputDto(user_id=user_id, user_name="heumsi", description="", password="1234")
    actual = user_application_service.update_user(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_delete_user_success(user_repository_mock, user_id, user_name, password):
    user_repository_mock.delete_by_user_id.return_value = None
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = DeleteUserInputDto(user_id=user_id)
    actual = user_application_service.delete_user(input_dto)
    expected = DeleteUserOutputDto()
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_delete_user_fail(user_repository_mock, user_id, user_name, password):
    user_repository_mock.delete_by_user_id.side_effect = ResourceNotFoundError()
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = DeleteUserInputDto(user_id=user_id)
    actual = user_application_service.delete_user(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_login_success(user_repository_mock, user_id, user_name, password):
    user_repository_mock.find_by_user_id.return_value = User(
        id=UserId(value=user_id),
        name=UserName(value=user_name),
        password="$2b$12$.fqrWFYdw.HLyHFfApiAx.NpOoTD6NcxJNWq5PWf7fu2cG5nheutG",
    )
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = LoginInputDto(user_id=user_id, password=password)
    actual = user_application_service.login(input_dto)
    expected = LoginOutputDto()
    assert actual == expected


def test_login_fail_with_wrong_id(user_repository_mock):
    wrong_user_id = "joon"
    user_repository_mock.find_by_user_id.side_effect = ResourceNotFoundError(f"{wrong_user_id}의 유저를 찾지 못했습니다.")
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = LoginInputDto(user_id=wrong_user_id, password="dump password")
    actual = user_application_service.login(input_dto)
    expected = FailedOutputDto.build_resource_not_found_error(message=f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다.")
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_login_fail_with_wrong_password(user_repository_mock, user_id, user_name, password):
    wrong_password = "wrong password"
    user_repository_mock.find_by_user_id.return_value = User(
        id=UserId(value=user_id),
        name=UserName(value=user_name),
        password="$2b$12$.fqrWFYdw.HLyHFfApiAx.NpOoTD6NcxJNWq5PWf7fu2cG5nheutG",
    )
    user_application_service = UserApplicationService(user_repository=user_repository_mock)

    input_dto = LoginInputDto(user_id=user_id, password=wrong_password)
    actual = user_application_service.login(input_dto)
    expected = FailedOutputDto.build_unauthorized_error(message=f"잘못된 비밀번호 입니다.")
    assert actual == expected
