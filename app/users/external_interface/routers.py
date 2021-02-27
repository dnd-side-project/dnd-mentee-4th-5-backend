from typing import Optional, Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header
from starlette import status
from starlette.responses import JSONResponse

from auth.application.dtos import GetTokenDataInputDto
from auth.application.service import AuthApplicationService
from container import Container
from shared_kernel.external_interface.json_dtos import FailedJsonResponse
from users.application.dtos import CreateUserInputDto, DeleteUserInputDto, FindUserInputDto, UpdateUserInputDto
from users.application.service import UserApplicationService
from users.external_interface.json_dtos import (
    CreateUserJsonRequest,
    CreateUserJsonResponse,
    GetUserJsonResponse,
    UpdateUserJsonRequest,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateUserJsonResponse)
@inject
def create_user(
    request: CreateUserJsonRequest,
    user_application_service: UserApplicationService = Depends(Provide[Container.user_application_service]),
) -> Union[CreateUserJsonResponse, JSONResponse]:
    input_dto = CreateUserInputDto(
        user_id=request.user_id,
        user_name=request.user_name,
        password=request.password,
    )
    output_dto = user_application_service.create_user(input_dto=input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    return CreateUserJsonResponse.build_by_ouput_dto(output_dto)
    # 원래는 아래처럼 주어야 하는데... 깔끔한 방식이 떠오르지 않아 현재는 아래 방식을 사용하지 않음.
    # return JSONResponse(status_code=status.HTTP_201_CREATED, headers={"Location": f"/users/{request.user_id}"})


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=GetUserJsonResponse)
@inject
def get_user(
    user_id: str,
    user_application_service: UserApplicationService = Depends(Provide[Container.user_application_service]),
) -> Union[GetUserJsonResponse, JSONResponse]:
    input_dto = FindUserInputDto(user_id=user_id)
    output_dto = user_application_service.find_user(input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    return GetUserJsonResponse.build_by_ouput_dto(output_dto)


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
@inject
def update_user(
    request: UpdateUserJsonRequest,
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(Provide[Container.auth_application_service]),
    user_application_service: UserApplicationService = Depends(Provide[Container.user_application_service]),
) -> Optional[JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(get_token_data_input_dto)
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = UpdateUserInputDto(
        user_id=get_token_data_output_dto.user_id,
        user_name=request.user_name,
        description=request.description,
        password=request.password,
    )
    output_dto = user_application_service.update_user(input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_user(
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(Provide[Container.auth_application_service]),
    user_application_service: UserApplicationService = Depends(Provide[Container.user_application_service]),
) -> Optional[JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(get_token_data_input_dto)
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = DeleteUserInputDto(user_id=get_token_data_output_dto.user_id)
    output_dto = user_application_service.delete_user(input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
