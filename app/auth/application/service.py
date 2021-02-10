from typing import Union

from jose import JWTError, jwt

from auth.application.dtos import (
    GetTokenDataInputDto,
    GetTokenDataOutputDto,
    GetTokenInputDto,
    GetTokenOutputDto,
    VerifyTokenInputDto,
    VerifyTokenOutputDto,
)
from auth.domain.value_objects import TokenPayload
from settings import Settings
from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import LoginInputDto
from users.application.service import UserApplicationService


class AuthApplicationService:
    def __init__(self, user_application_service: UserApplicationService, settings: Settings) -> None:
        self._user_application_service = user_application_service
        self._JWT_SECRET_KEY = settings.JWT_SECRET_KEY
        self._JWT_ALGORITHM = settings.JWT_ALGORITHM

    def get_token(self, input_dto: GetTokenInputDto) -> Union[GetTokenOutputDto, FailedOutputDto]:
        try:
            login_input_dto = LoginInputDto(user_id=input_dto.user_id, password=input_dto.password)
            login_output_dto = self._user_application_service.login(input_dto=login_input_dto)

            if login_output_dto.status is True:
                access_token = self._create_access_token(data=TokenPayload(user_id=input_dto.user_id).dict())
                return GetTokenOutputDto(access_token=access_token)
            return FailedOutputDto.build_resource_error(message=login_output_dto.message)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def get_token_data(self, input_dto: GetTokenDataInputDto) -> Union[GetTokenDataOutputDto, FailedOutputDto]:
        try:
            decoded_jwt = jwt.decode(
                token=input_dto.access_token,
                key=self._JWT_SECRET_KEY,
                algorithms=self._JWT_ALGORITHM,
            )
            token_payload = TokenPayload(**decoded_jwt)
            return GetTokenDataOutputDto(user_id=token_payload.user_id)
        except JWTError:
            return FailedOutputDto.build_unauthorized_error(message="올바른 access-token이 아닙니다.")

    def verify_token(self, input_dto: VerifyTokenInputDto) -> Union[VerifyTokenOutputDto, FailedOutputDto]:
        """
        현재 사용하지 않음.
        """
        try:
            decoded_jwt = jwt.decode(
                token=input_dto.access_token,
                key=self._JWT_SECRET_KEY,
                algorithms=self._JWT_ALGORITHM,
            )
            if TokenPayload(**decoded_jwt) == TokenPayload(user_id=input_dto.user_id):
                return VerifyTokenOutputDto()
            return FailedOutputDto.build_unauthorized_error(message="access-token이 유효하지 않습니다.")
        except JWTError:
            return FailedOutputDto.build_unauthorized_error(message="올바른 access-token이 아닙니다.")
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def _create_access_token(self, data: dict) -> str:
        try:
            encoded_jwt = jwt.encode(data, self._JWT_SECRET_KEY, algorithm=self._JWT_ALGORITHM)
            return encoded_jwt
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
