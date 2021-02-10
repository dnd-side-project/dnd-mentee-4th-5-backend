from typing import Optional, Union

from passlib.context import CryptContext

from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import (
    CreateUserInputDto,
    DeleteUserInputDto,
    FindUserInputDto,
    FindUserOutputDto,
    LoginInputDto,
    LoginOutputDto,
    UpdateUserInputDto,
    CreateUserOutputDto,
    UpdateUserOutputDto,
    DeleteUserOutputDto,
)
from users.domain.entities import User
from users.domain.repository import UserRepository
from users.domain.value_objects import UserId, UserName


class UserApplicationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def find_user(self, input_dto: FindUserInputDto) -> Union[FindUserOutputDto, FailedOutputDto]:
        try:
            user = self._user_repository.find_by_user_id(user_id=UserId(value=input_dto.user_id))
            if user is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다."
                )
            return FindUserOutputDto(
                user_id=str(user.id),
                user_name=str(user.name),
                description=user.description,
                image_url=user.image_url,
            )
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_user(self, input_dto: CreateUserInputDto) -> Union[CreateUserOutputDto, FailedOutputDto]:
        try:
            user = User(
                id=UserId(value=input_dto.user_id),
                name=UserName(value=input_dto.user_name),
                password=self._get_password_hash(input_dto.password),
            )
            if self._user_repository.find_by_user_id(user.id) is not None:
                return FailedOutputDto.build_resource_conflict_error(f"{str(user.id)}는 이미 존재하는 유저입니다.")
            self._user_repository.add(user)
            return CreateUserOutputDto(
                user_id=str(user.id),
                user_name=str(user.name),
                description=user.description,
                image_url=user.image_url,
            )
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_user(self, input_dto: UpdateUserInputDto) -> Union[UpdateUserOutputDto, FailedOutputDto]:
        try:
            user = User(
                id=UserId(value=input_dto.user_id),
                name=UserName(value=input_dto.user_name),
                description=input_dto.description,
                password=input_dto.password,
            )
            if not self._user_repository.find_by_user_id(user.id):
                return FailedOutputDto.build_resource_not_found_error(f"{str(user.id)}의 유저를 찾지 못했습니다.")
            self._user_repository.update(user)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
        return UpdateUserOutputDto()

    def delete_user(self, input_dto: DeleteUserInputDto) -> Union[DeleteUserOutputDto, FailedOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            if not self._user_repository.find_by_user_id(user_id):
                return FailedOutputDto.build_resource_not_found_error(f"{str(user_id)}의 유저를 찾지 못했습니다.")
            self._user_repository.delete_by_user_id(user_id)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
        return DeleteUserOutputDto()

    def login(self, input_dto: LoginInputDto) -> Union[LoginOutputDto, FailedOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            user = self._user_repository.find_by_user_id(user_id=user_id)
            if user is None:
                return FailedOutputDto.build_resource_not_found_error(f"{str(user_id)}의 유저를 찾지 못했습니다.")

            if not self._verify_password(input_dto.password, user.password):
                return FailedOutputDto.build_unauthorized_error(f"잘못된 비밀번호 입니다.")
            return LoginOutputDto()
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def _get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
