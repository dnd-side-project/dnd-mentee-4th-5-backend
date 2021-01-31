from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from users.infra_structure.container import Container
from users.application.dtos import CreateUserInputDto
from users.application.service import UserApplicationService
from users.domain.repository import UserRepository
from users.domain.value_objects import UserId, UserName
from users.external_interface.json_dto import CreateUserJsonRequest

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("")
@inject
def create_user(
    request: CreateUserJsonRequest,
    user_repository: UserRepository = Depends(Provide[Container.user_repository]),
):
    user_application_service = UserApplicationService(user_repository=user_repository)
    input_dto = CreateUserInputDto(
        user_id=UserId(value=request.user_id),
        user_name=UserName(value=request.user_name),
        hashed_password=request.hashed_password,
    )
    user_application_service.create_user(input_dto=input_dto)
