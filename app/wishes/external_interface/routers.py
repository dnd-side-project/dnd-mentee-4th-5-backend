from typing import Union, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header
from starlette import status
from starlette.responses import JSONResponse

from auth.application.dtos import GetTokenDataInputDto
from auth.application.service import AuthApplicationService
from container import Container
from drinks.application.service import DrinkApplicationService
from shared_kernel.external_interface.json_dtos import FailedJsonResponse
from wishes.application.dto import CreateWishInputDto, DeleteWishInputDto, FindWishesInputDto
from wishes.application.service import WishApplicationService
from wishes.domain.repository import QueryParam
from wishes.external_interface.json_dtos import CreateWishJsonResponse, GetWishesJsonResponse

router = APIRouter(
    prefix="/wishes",
    tags=["wishes"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetWishesJsonResponse])
@inject
def get_wishes(
    query_param: QueryParam = Depends(),
    wish_application_service: WishApplicationService = Depends(Provide[Container.wish_application_service]),
):
    input_dto = FindWishesInputDto(query_param=query_param)
    output_dto = wish_application_service.find_wishes(input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    return GetWishesJsonResponse.build_by_output_dto(output_dto)


@router.post("/{drink_id}", status_code=status.HTTP_201_CREATED, response_model=CreateWishJsonResponse)
@inject
def create_wish(
    drink_id: str,
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(Provide[Container.auth_application_service]),
    wish_application_service: WishApplicationService = Depends(Provide[Container.wish_application_service]),
    drink_application_service: DrinkApplicationService = Depends(Provide[Container.drink_application_service]),
) -> Union[CreateWishJsonResponse, JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(get_token_data_input_dto)
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = CreateWishInputDto(user_id=get_token_data_output_dto.user_id, drink_id=drink_id)
    output_dto = wish_application_service.create_wish(input_dto, drink_application_service)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    return CreateWishJsonResponse.build_by_output_dto(output_dto)


@router.delete("/{wish_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_wish(
    wish_id: str,
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(Provide[Container.auth_application_service]),
    wish_application_service: WishApplicationService = Depends(Provide[Container.wish_application_service]),
    drink_application_service: DrinkApplicationService = Depends(Provide[Container.drink_application_service]),
) -> Union[CreateWishJsonResponse, JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(get_token_data_input_dto)
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = DeleteWishInputDto(wish_id=wish_id)
    output_dto = wish_application_service.delete_wish(input_dto, drink_application_service)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
