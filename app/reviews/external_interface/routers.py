from typing import Optional, Union

from auth.application.dtos import GetTokenDataInputDto
from auth.application.service import AuthApplicationService
from container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header
from reviews.application.dtos import (CreateReviewInputDto,
                                      DeleteReviewInputDto, FindReviewInputDto,
                                      FindReviewOutputDto,
                                      UpdateReviewInputDto)
from reviews.application.service import ReviewApplicationService
from reviews.external_interface.json_dtos import (CreateReviewJsonRequest,
                                                  CreateReviewJsonResponse,
                                                  DeleteReviewJsonRequest,
                                                  GetReviewJsonResponse,
                                                  GetReviewsJsonResponse,
                                                  UpdateReviewJsonRequest)
from shared_kernel.external_interface.json_dto import FailedJsonResponse
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get("/{review_id}", status_code=status.HTTP_200_OK)
@inject
def get_review(
    review_id: str,
    review_application_service: ReviewApplicationService = Depends(
        Provide[Container.review_application_service]
    ),
) -> Union[GetReviewJsonResponse, JSONResponse]:
    input_dto = FindReviewInputDto(review_id=review_id)
    output_dto = review_application_service.find_review(input_dto=input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    return GetReviewJsonResponse.build_by_ouput_dto(output_dto)


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetReviewsJsonResponse)
@inject
def get_reviews(
    user_id: Optional[str],
    drink_id: Optional[str],
    review_application_service: ReviewApplicationService = Depends(
        Provide[Container.review_application_service]
    ),
) -> Union[GetReviewsJsonResponse, JSONResponse]:
    # TODO: 내부 로직 짜야 함.
    return GetReviewsJsonResponse(
        values=[
            FindReviewOutputDto(
                review_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
                drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
                user_id="heumsi",
                rating=4,
                comment="",
                created_at=1355563265.81,
                updated_at=1355563265.81,
            )
        ]
    )


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=CreateReviewJsonResponse
)
@inject
def create_review(
    request: CreateReviewJsonRequest,
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(
        Provide[Container.auth_application_service]
    ),
    review_application_service: ReviewApplicationService = Depends(
        Provide[Container.review_application_service]
    ),
) -> Union[CreateReviewJsonResponse, JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(
        get_token_data_input_dto
    )
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = CreateReviewInputDto(
        drink_id=request.drink_id,
        user_id=get_token_data_output_dto.user_id,
        rating=request.rating,
        comment=request.comment,
    )
    output_dto = review_application_service.create_review(input_dto=input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
    return CreateReviewJsonResponse.build_by_ouput_dto(output_dto)


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
@inject
def update_review(
    request: UpdateReviewJsonRequest,
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(
        Provide[Container.auth_application_service]
    ),
    review_application_service: ReviewApplicationService = Depends(
        Provide[Container.review_application_service]
    ),
) -> Optional[JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(
        get_token_data_input_dto
    )
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = UpdateReviewInputDto(
        review_id=request.review_id, rating=request.rating, comment=request.comment
    )
    output_dto = review_application_service.update_review(input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_review(
    request: DeleteReviewJsonRequest,
    access_token: str = Header(...),
    auth_application_service: AuthApplicationService = Depends(
        Provide[Container.auth_application_service]
    ),
    review_application_service: ReviewApplicationService = Depends(
        Provide[Container.review_application_service]
    ),
) -> Optional[JSONResponse]:
    get_token_data_input_dto = GetTokenDataInputDto(access_token=access_token)
    get_token_data_output_dto = auth_application_service.get_token_data(
        get_token_data_input_dto
    )
    if not get_token_data_output_dto.status:
        return FailedJsonResponse.build_by_output_dto(get_token_data_output_dto)

    input_dto = DeleteReviewInputDto(review_id=request.review_id)
    output_dto = review_application_service.delete_review(input_dto)
    if not output_dto.status:
        return FailedJsonResponse.build_by_output_dto(output_dto)
