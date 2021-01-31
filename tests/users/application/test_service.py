import pytest

from users.application.dtos import (
    CreateUserInputDto,
    UpdateUserInputDto,
    DeleteUserInputDto,
    FindUserInputDto,
    FindUserOutputDto,
    LoginInputDto,
    LoginOutputDto,
)
from users.application.service import UserApplicationService
from users.domain.entities import User
from users.application.exceptions import UserNotExistError
from users.domain.value_objects import UserId, UserName, LoginStatus
from users.infra_structure.in_memory_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_application_service(user_repository):
    return UserApplicationService(user_repository=user_repository)


user_data = [("heumsi", "heumsi", "1234")]


@pytest.mark.parametrize("user_id, user_name, hashed_password", user_data)
def test_find_user(user_application_service, user_repository, user_id, user_name, hashed_password):
    user_repository.add(
        User(id=UserId(value=user_id), name=UserName(value=user_name), hashed_password=hashed_password)
    )

    input_dto = FindUserInputDto(user_id=UserId(value=user_id))
    actual = user_application_service.find_user(input_dto)
    expected = FindUserOutputDto(
        user_id=UserId(value=user_id),
        user_name=UserName(value=user_name),
        description="",
        hashed_password=hashed_password,
        image_url="",
    )
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, hashed_password", user_data)
def test_create_user(user_application_service, user_repository, user_id, user_name, hashed_password):
    input_dto = CreateUserInputDto(
        user_id=UserId(value="heumsi"), user_name=UserName(value="heumsi"), hashed_password="1234"
    )
    user_application_service.create_user(input_dto)

    actual = user_repository.find_all()
    expected = [User(id=UserId(value="heumsi"), name=UserName(value="heumsi"), hashed_password="1234")]
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, hashed_password", user_data)
def test_update_user(user_application_service, user_repository, user_id, user_name, hashed_password):
    user_repository.add(
        User(id=UserId(value=user_id), name=UserName(value=user_name), hashed_password=hashed_password)
    )

    input_dto = UpdateUserInputDto(
        user_id=UserId(value=user_id),
        user_name=UserName(value="siheum"),
        description="hi, I'm siheum!",
        hashed_password="4321",
        image_url="",
    )
    user_application_service.update_user(input_dto)

    actual = user_repository.find_by_user_id(user_id=UserId(value=user_id))
    expected = User(
        id=UserId(value=user_id),
        name=UserName(value="siheum"),
        description="hi, I'm siheum!",
        hashed_password="4321",
        image_url="",
    )
    assert actual == expected


@pytest.mark.parametrize("user_id, user_name, hashed_password", user_data)
def test_delete_user(user_application_service, user_repository, user_id, user_name, hashed_password):
    user_repository.add(
        User(id=UserId(value=user_id), name=UserName(value=user_name), hashed_password=hashed_password)
    )

    input_dto = DeleteUserInputDto(user_id=UserId(value=user_id))
    user_application_service.delete_user(input_dto)

    actual = user_repository.find_by_user_id(user_id=UserId(value=user_id))
    expected = None
    assert actual == expected

    # Check delete user when user in-memory repo is Empty
    with pytest.raises(UserNotExistError):
        user_application_service.delete_user(input_dto)


@pytest.mark.parametrize("user_id, user_name, hashed_password", user_data)
def test_login(user_application_service, user_repository, user_id, user_name, hashed_password):
    user_repository.add(
        User(id=UserId(value=user_id), name=UserName(value=user_name), hashed_password=hashed_password)
    )

    input_dto = LoginInputDto(user_id=UserId(value=user_id), hashed_password=hashed_password)
    actual = user_application_service.login(input_dto)
    expected = LoginOutputDto(status=LoginStatus.SUCCESS)
    assert actual == expected

    # Wrong Id
    input_dto = LoginInputDto(user_id=UserId(value="joon"), hashed_password=hashed_password)
    actual = user_application_service.login(input_dto)
    expected = LoginOutputDto(status=LoginStatus.FAILED, message=f"{str(input_dto.user_id)} 아이디는 존재하지 않습니다.")
    assert actual == expected

    # Wrong PW
    input_dto = LoginInputDto(user_id=UserId(value=user_id), hashed_password="4321")
    actual = user_application_service.login(input_dto)
    expected = LoginOutputDto(status=LoginStatus.FAILED, message=f"잘못된 비밀번호 입니다.")
    assert actual == expected
