from typing import List

from pydantic import BaseModel


class FindReviewInputDto(BaseModel):
    review_id: str


class FindReviewOutputDto(BaseModel):
    review_id: str
    drink_id: str
    user_id: str
    rating: int
    comment: str
    created_at: float


class CreateReviewInputDto(BaseModel):
    drink_id: str
    user_id: str
    rating: int
    comment: str
    created_at: float


class UpdateReviewInputDto(BaseModel):
    review_id: str
    drink_id: str
    user_id: str
    rating: int
    comment: str
    created_at: float


class DeleteReviewInputDto(BaseModel):
    review_id: str


class FindReviewsByUserIdInputDto(BaseModel):
    user_id: str


class FindReviewsByUserIdOutputDto(BaseModel):
    reviews_dicts: List[dict]


class FindReviewsByDrinkIdInputDto(BaseModel):
    drink_id: str


class FindReviewsByDrinkIdOutputDto(BaseModel):
    reviews_dicts: List[dict]
