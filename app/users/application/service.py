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
from users.application.exceptions import UserAlreadyExistError, UserNotExistError
from users.domain.repository import UserRepository
from users.domain.value_objects import LoginStatus


class UserApplicationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def find_user(self, input_dto: FindUserInputDto) -> FindUserOutputDto:
        user = self._user_repository.find_by_user_id(input_dto.user_id)
        if user is None:
            raise UserNotExistError(f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다.")
        return FindUserOutputDto(
            user_id=input_dto.user_id,
            user_name=user.name,
            description=user.description,
            hashed_password=user.hashed_password,
            image_url=user.image_url,
            review_ids=user.review_ids,
            wished_drinks_ids=user.wished_drinks_ids,
        )

    def create_user(self, input_dto: CreateUserInputDto) -> None:
        user = User(
            id=input_dto.user_id,
            name=input_dto.user_name,
            hashed_password=input_dto.hashed_password,
        )

        if self._user_repository.find_by_user_id(user_id=input_dto.user_id) is not None:
            raise UserAlreadyExistError(f"{str(input_dto.user_id)}는 이미 존재하는 유저입니다.")
        self._user_repository.add(user)

    def update_user(self, input_dto: UpdateUserInputDto) -> None:
        user = User(
            id=input_dto.user_id,
            name=input_dto.user_name,
            description=input_dto.description,
            hashed_password=input_dto.hashed_password,
            image_url=input_dto.image_url,
        )

        if not self._user_repository.find_by_user_id(user_id=input_dto.user_id):
            raise UserNotExistError(f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다.")
        self._user_repository.update(user)

    def delete_user(self, input_dto: DeleteUserInputDto) -> None:
        user_id = input_dto.user_id
        if not self._user_repository.find_by_user_id(user_id=user_id):
            raise UserNotExistError(f"{str(input_dto.user_id)}의 유저를 찾지 못했습니다.")
        self._user_repository.delete_by_user_id(user_id=user_id)

    def login(self, input_dto: LoginInputDto) -> LoginOutputDto:
        user = self._user_repository.find_by_user_id(input_dto.user_id)
        if user is None:
            return LoginOutputDto(status=LoginStatus.FAILED, message=f"{str(input_dto.user_id)} 아이디는 존재하지 않습니다.")

        if not user.hashed_password == input_dto.hashed_password:
            return LoginOutputDto(status=LoginStatus.FAILED, message=f"잘못된 비밀번호 입니다.")

        return LoginOutputDto(status=LoginStatus.SUCCESS)
