from typing import Optional, Union

from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import (
    CreateUserInputDto,
    UpdateUserInputDto,
    DeleteUserInputDto,
    FindUserInputDto,
    FindUserOutputDto,
    LoginInputDto,
    LoginOutputDto,
)
from users.domain.entities import User
from users.domain.repository import UserRepository
from users.domain.value_objects import UserId, UserName


class UserApplicationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def find_user(self, input_dto: FindUserInputDto) -> Optional[FindUserOutputDto]:
        try:
            user = self._user_repository.find_by_user_id(user_id=UserId(value=input_dto.user_id))
            if user is None:
                return FailedOutputDto.build_resource_error(message=f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다.")
            return FindUserOutputDto(
                user_id=str(user.id),
                user_name=str(user.name),
                description=user.description,
                password=user.password,
                image_url=user.image_url,
            )
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_user(self, input_dto: CreateUserInputDto) -> Optional[FailedOutputDto]:
        try:
            user = User(
                id=UserId(value=input_dto.user_id),
                name=UserName(value=input_dto.user_name),
                password=input_dto.password,
            )

            if self._user_repository.find_by_user_id(user.id) is not None:
                return FailedOutputDto.build_resource_error(f"{str(user.id)}는 이미 존재하는 유저입니다.")
            self._user_repository.add(user)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_user(self, input_dto: UpdateUserInputDto) -> Optional[FailedOutputDto]:
        try:
            user = User(
                id=UserId(value=input_dto.user_id),
                name=UserName(value=input_dto.user_name),
                description=input_dto.description,
                password=input_dto.password,
                image_url=input_dto.image_url,
            )
            if not self._user_repository.find_by_user_id(user.id):
                return FailedOutputDto.build_resource_error(f"{str(user.id)}의 유저를 찾지 못했습니다.")
            self._user_repository.update(user)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_user(self, input_dto: DeleteUserInputDto) -> Optional[FailedOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            if not self._user_repository.find_by_user_id(user_id):
                return FailedOutputDto.build_resource_error(f"{str(user_id)}의 유저를 찾지 못했습니다.")
            self._user_repository.delete_by_user_id(user_id)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def login(self, input_dto: LoginInputDto) -> Union[LoginOutputDto, FailedOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            user = self._user_repository.find_by_user_id(user_id=user_id)
            if user is None:
                return FailedOutputDto.build_resource_error(f"{str(user_id)}의 유저를 찾지 못했습니다.")

            if not user.password == input_dto.password:
                return FailedOutputDto.build_resource_error(f"잘못된 비밀번호 입니다.")

            return LoginOutputDto()
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
