from typing import List

from pydantic import BaseModel
from reviews.domain.repository import QueryParam
from shared_kernel.application.dtos import SuccessOutputDto


class FindReviewInputDto(BaseModel):
    review_id: str


class FindReviewOutputDto(SuccessOutputDto):
    review_id: str
    drink_id: str
    user_id: str
    rating: int
    comment: str
    created_at: float
    updated_at: float


class FindReviewsInputDto(BaseModel):
    query_param: QueryParam


class FindReviewsOutputDto(SuccessOutputDto):
    class Item(BaseModel):
        review_id: str
        drink_id: str
        user_id: str
        rating: int
        comment: str
        created_at: float
        updated_at: float

    items: List[Item]


class CreateReviewInputDto(BaseModel):
    drink_id: str
    user_id: str
    rating: int
    comment: str


class CreateReviewOutputDto(SuccessOutputDto):
    review_id: str
    drink_id: str
    user_id: str
    rating: int
    comment: str
    created_at: float
    updated_at: float


class UpdateReviewInputDto(BaseModel):
    review_id: str
    rating: int
    comment: str


class UpdateReviewOutputDto(SuccessOutputDto):
    pass


class DeleteReviewInputDto(BaseModel):
    review_id: str


class DeleteReviewOutputDto(SuccessOutputDto):
    pass
