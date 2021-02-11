from typing import List

from pydantic import BaseModel

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


class CreateReviewInputDto(BaseModel):
    drink_id: str
    user_id: str
    rating: int
    comment: str


class CreateReviewOutputDto(SuccessOutputDto):
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


class FindReviewsByUserIdInputDto(BaseModel):
    user_id: str


class FindReviewsByUserIdOutputDto(BaseModel):
    reviews_dicts: List[dict]


class FindReviewsByDrinkIdInputDto(BaseModel):
    drink_id: str


class FindReviewsByDrinkIdOutputDto(BaseModel):
    reviews_dicts: List[dict]
