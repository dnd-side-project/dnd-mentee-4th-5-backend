from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from shared_kernel.external_interface.json_dto import FailedJsonResponse
from container import Container
from users.application.dtos import CreateUserInputDto
from users.application.service import UserApplicationService
from users.domain.repository import UserRepository
from users.external_interface.json_dto import CreateUserJsonRequest

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    request: CreateUserJsonRequest,
    user_repository: UserRepository = Depends(Provide[Container.user_repository]),
):
    user_application_service = UserApplicationService(user_repository=user_repository)
    input_dto = CreateUserInputDto(
        user_id=request.user_id,
        user_name=request.user_name,
        password=request.password,
    )
    output_dto = user_application_service.create_user(input_dto=input_dto)
    if output_dto is not None:
        return FailedJsonResponse.build_by_output_dto(output_dto)
