from passlib.context import CryptContext
from jose import jwt

from app.auth.application.dtos import GetTokenInputDto, GetTokenOutputDto
from app.users.application.service import UserApplicationService
from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import LoginInputDto


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


class AuthApplicationService:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    def __init__(self, user_application_service: UserApplicationService):
        self._user_application_service = user_application_service

    def get_token(
        self,
        input_dto: GetTokenInputDto,
    ) -> [GetTokenOutputDto, FailedOutputDto]:

        login_input_dto = LoginInputDto(user_id=input_dto.user_id, password=input_dto.password)
        login_output_dto = self._user_application_service.login(input_dto=login_input_dto)

        if login_output_dto.status is True:
            access_token = self._create_access_token(data={"user_id": input_dto.user_id})
            return GetTokenOutputDto(access_token=access_token)
        return FailedOutputDto.build_resource_error(message=login_output_dto.message)

    def _create_access_token(self, data: dict) -> str:
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
