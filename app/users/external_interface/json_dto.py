from pydantic import BaseModel

from users.application.dtos import FindUserOutputDto, CreateUserOutputDto


class GetUserJsonResponse(BaseModel):
    user_id: str
    user_name: str
    description: str
    image_url: str

    @classmethod
    def build_by_ouput_dto(cls, output_dto: FindUserOutputDto) -> "GetUserJsonResponse":
        return cls(
            user_id=output_dto.user_id,
            user_name=output_dto.user_name,
            description=output_dto.description,
            image_url=output_dto.image_url,
        )


class CreateUserJsonRequest(BaseModel):
    user_id: str
    user_name: str
    password: str


class CreateUserJsonResponse(BaseModel):
    user_id: str
    user_name: str
    description: str
    image_url: str

    @classmethod
    def build_by_ouput_dto(cls, output_dto: CreateUserOutputDto) -> "CreateUserJsonResponse":
        return cls(
            user_id=output_dto.user_id,
            user_name=output_dto.user_name,
            description=output_dto.description,
            image_url=output_dto.image_url,
        )


class UpdateUserJsonRequest(BaseModel):
    user_name: str
    description: str
    password: str


class UpdateUserJsonResponse(BaseModel):
    user_name: str
    description: str


class DeleteUserJsonResponse(BaseModel):
    user_id: str
    user_name: str
    description: str
