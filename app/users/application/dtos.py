from pydantic import BaseModel, Field

from shared_kernel.application.dtos import SuccessOutputDto


class FindUserInputDto(BaseModel):
    user_id: str


class FindUserOutputDto(SuccessOutputDto):
    user_id: str
    user_name: str
    description: str
    password: str
    image_url: str


class CreateUserInputDto(BaseModel):
    user_id: str
    user_name: str
    password: str


class UpdateUserInputDto(SuccessOutputDto):
    user_id: str
    user_name: str
    description: str
    password: str
    image_url: str


class DeleteUserInputDto(BaseModel):
    user_id: str


class LoginInputDto(BaseModel):
    user_id: str
    password: str


class LoginOutputDto(SuccessOutputDto):
    message: str = Field(default="")
