from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from auth.application.dtos import GetTokenInputDto
from auth.external_interface.json_dto import GetTokenJsonRequest, GetTokenJsonResponse
from container import Container
from shared_kernel.external_interface.json_dto import FailedJsonResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/token", status_code=status.HTTP_200_OK)
@inject
def get_token(
    request: GetTokenJsonRequest, auth_application_service=Depends(Provide[Container.auth_application_service])
):
    input_dto = GetTokenInputDto(
        user_id=request.user_id,
        password=request.password,
    )
    output_dto = auth_application_service.get_token(input_dto=input_dto)
    if output_dto.status:
        return GetTokenJsonResponse(access_token=output_dto.access_token)
    return FailedJsonResponse.build_by_output_dto(output_dto)
