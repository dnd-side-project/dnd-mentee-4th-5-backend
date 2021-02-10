import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from reviews.application.dtos import CreateReviewInputDto
from reviews.application.service import ReviewApplicationService
from reviews.domain.repository import ReviewRepository
from reviews.domain.value_objects import ReviewRating, UserId
from reviews.infra_structure.container import Container

router = APIRouter(
    prefix="/users/reviews",
    tags=["reviews"],
)


@router.post("")
@inject
def create_review(
    request: CreateReviewJsonRequest,
    review_repository: ReviewRepository = Depends(Provide[Container.review_repository]),
):
    review_application_service = ReviewApplicationService(
        review_repository=review_repository
    )
    input_dto = CreateReviewInputDto(
        review_id=uuid.uuid4(),
        drink_id=request.drink_id,
        user_id=UserId(value=request.user_id),
        rating=ReviewRating(value=request.rating),
        comment=request.comment,
        created_at=request.created_at,
    )
    review_application_service.create_review(input_dto=input_dto)
