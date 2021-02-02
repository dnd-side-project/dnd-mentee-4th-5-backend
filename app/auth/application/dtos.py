from pydantic import BaseModel

from shared_kernel.application.dtos import SuccessOutputDto


class GetTokenInputDto(BaseModel):
    user_id: str
    password: str


class GetTokenOutputDto(SuccessOutputDto):
    access_token: str
