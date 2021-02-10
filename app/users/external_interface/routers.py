from container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from shared_kernel.external_interface.json_dto import FailedJsonResponse
from starlette import status
from users.application.dtos import CreateUserInputDto
from users.application.service import UserApplicationService
from users.external_interface.json_dto import CreateUserJsonRequest

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    request: CreateUserJsonRequest,
    user_application_service: UserApplicationService = Depends(
        Provide[Container.user_application_service]
    ),
):
    input_dto = CreateUserInputDto(
        user_id=request.user_id,
        user_name=request.user_name,
        password=request.password,
    )
    output_dto = user_application_service.create_user(input_dto=input_dto)
    if output_dto is not None:
        return FailedJsonResponse.build_by_output_dto(output_dto)
