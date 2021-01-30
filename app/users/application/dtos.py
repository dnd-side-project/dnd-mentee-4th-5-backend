from typing import List

from pydantic import BaseModel, Field

from users.domain.value_objects import UserId, UserName, LoginStatus


class FindUserInputDto(BaseModel):
    user_id: UserId


class FindUserOutputDto(BaseModel):
    user_id: UserId
    user_name: UserName
    description: str
    hashed_password: str
    image_url: str
    review_ids: List[str]
    wished_drinks_ids: List[str]


class CreateUserInputDto(BaseModel):
    user_id: UserId
    user_name: UserName
    hashed_password: str


class UpdateUserInputDto(BaseModel):
    user_id: UserId
    user_name: UserName
    description: str
    hashed_password: str
    image_url: str


class DeleteUserInputDto(BaseModel):
    user_id: UserId


class LoginInputDto(BaseModel):
    user_id: UserId
    hashed_password: str


class LoginOutputDto(BaseModel):
    status: LoginStatus
    message: str = Field(default="")
