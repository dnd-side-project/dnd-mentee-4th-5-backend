import pytest
from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import (
    CreateUserInputDto,
    DeleteUserInputDto,
    FindUserInputDto,
    FindUserOutputDto,
    LoginInputDto,
    LoginOutputDto,
    UpdateUserInputDto,
)
from users.application.service import UserApplicationService
from users.domain.entities import User
from users.domain.value_objects import UserId, UserName
from users.infra_structure.in_memory_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_application_service(user_repository):
    return UserApplicationService(user_repository=user_repository)


user_data = [("heumsi", "heumsi", "1234")]


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_find_user(user_application_service, user_repository, user_id, user_name, password):
    user_repository.add(User(id=UserId(value=user_id), name=UserName(value=user_name), password=password))

    input_dto = FindUserInputDto(user_id=user_id)
    actual = user_application_service.find_user(input_dto)
    expected = FindUserOutputDto(
        user_id=user_id,
        user_name=user_name,
        description="",
        password=password,
        image_url="",
    )
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_create_user(user_application_service, user_repository, user_id, user_name, password):
    input_dto = CreateUserInputDto(user_id=user_id, user_name=user_name, password=password)
    user_application_service.create_user(input_dto)

    actual = user_repository.find_all()
    expected = [User(id=UserId(value=user_id), name=UserName(value=user_name), password=password)]
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_update_user(user_application_service, user_repository, user_id, user_name, password):
    user_repository.add(User(id=UserId(value=user_id), name=UserName(value=user_name), password=password))

    input_dto = UpdateUserInputDto(
        user_id=user_id,
        user_name="siheum",
        description="hi, I'm siheum!",
        password="4321",
        image_url="",
    )
    user_application_service.update_user(input_dto)

    actual = user_repository.find_by_user_id(user_id=UserId(value=user_id))
    expected = User(
        id=UserId(value=user_id),
        name=UserName(value="siheum"),
        description="hi, I'm siheum!",
        password="4321",
        image_url="",
    )
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_delete_user(user_application_service, user_repository, user_id, user_name, password):
    user_repository.add(User(id=UserId(value=user_id), name=UserName(value=user_name), password=password))

    input_dto = DeleteUserInputDto(user_id=user_id)
    user_application_service.delete_user(input_dto)

    actual = user_repository.find_by_user_id(user_id=UserId(value=user_id))
    expected = None
    assert actual == expected

    # Check delete user when user in-memory repo is Empty
    output_dto = user_application_service.delete_user(input_dto)
    assert output_dto == FailedOutputDto.build_resource_error("heumsi의 유저를 찾지 못했습니다.")


@pytest.mark.parametrize("user_id, user_name, password", user_data)
def test_login(user_application_service, user_repository, user_id, user_name, password):
    user_repository.add(User(id=UserId(value=user_id), name=UserName(value=user_name), password=password))

    input_dto = LoginInputDto(user_id=user_id, password=password)
    actual = user_application_service.login(input_dto)
    expected = LoginOutputDto()
    assert actual == expected

    # Wrong Id
    input_dto = LoginInputDto(user_id="joon", password=password)
    actual = user_application_service.login(input_dto)
    expected = FailedOutputDto.build_resource_error(message=f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다.")
    assert actual == expected

    # Wrong PW
    input_dto = LoginInputDto(user_id=user_id, password="4321")
    actual = user_application_service.login(input_dto)
    expected = FailedOutputDto.build_resource_error(message=f"잘못된 비밀번호 입니다.")
    assert actual == expected
