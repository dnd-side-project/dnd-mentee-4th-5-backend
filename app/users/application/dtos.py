from pydantic import BaseModel

from shared_kernel.application.dtos import SuccessOutputDto


class FindUserInputDto(BaseModel):
    user_id: str


class FindUserOutputDto(SuccessOutputDto):
    user_id: str
    user_name: str
    description: str
    image_url: str


class CreateUserInputDto(BaseModel):
    user_id: str
    user_name: str
    password: str


class CreateUserOutputDto(SuccessOutputDto):
    user_id: str
    user_name: str
    description: str
    image_url: str


class UpdateUserInputDto(BaseModel):
    user_id: str
    user_name: str
    description: str
    password: str


class UpdateUserOutputDto(SuccessOutputDto):
    pass


class DeleteUserInputDto(BaseModel):
    user_id: str


class DeleteUserOutputDto(SuccessOutputDto):
    pass


class LoginInputDto(BaseModel):
    user_id: str
    password: str


class LoginOutputDto(SuccessOutputDto):
    pass
