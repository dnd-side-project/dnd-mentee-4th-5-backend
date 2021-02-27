from typing import Optional, Union, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from container import Container
from drinks.application.dtos import CreateDrinkInputDto, FindDrinksInputDto
from drinks.application.service import DrinkApplicationService
from drinks.domain.repository import QueryParam
from drinks.external_interface.json_dto import (
    CreateDrinkJsonRequest,
    GetDrinkJsonResponse,
)
from shared_kernel.external_interface.json_dto import FailedJsonResponse

router = APIRouter(
    prefix="/drinks",
    tags=["drinks"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_drink(
    request: CreateDrinkJsonRequest,
    drink_application_service: DrinkApplicationService = Depends(Provide[Container.drink_application_service]),
) -> Optional[JSONResponse]:
    input_dto = CreateDrinkInputDto(
        drink_name=request.drink_name,
        drink_image_url=request.drink_image_url,
        drink_type=request.drink_type,
    )
    output_dto = drink_application_service.create_drink(input_dto=input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[GetDrinkJsonResponse])
@inject
def get_drinks(
    query_param: QueryParam = Depends(),
    drink_application_service: DrinkApplicationService = Depends(Provide[Container.drink_application_service]),
) -> Union[List[GetDrinkJsonResponse], JSONResponse]:
    input_dto = FindDrinksInputDto(query_param=query_param.to_enum())
    output_dto = drink_application_service.find_drinks(input_dto=input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    get_drinks_json_response = [GetDrinkJsonResponse.build_by_output_dto(review) for review in output_dto.items]
    return get_drinks_json_response
