from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from reviews.domain.value_objects import ReviewRating
from users.domain.value_objects import UserId


class FindReviewInputDto(BaseModel):
    review_id: UUID


class FindReviewOutputDto(BaseModel):
    review_id: UUID
    drink_id: UUID
    user_id: UserId
    rating: ReviewRating
    comment: str
    created_at: float


class CreateReviewInputDto(BaseModel):
    review_id: UUID
    drink_id: UUID
    user_id: UserId
    rating: ReviewRating
    comment: str
    created_at: float


class UpdateReviewInputDto(BaseModel):
    review_id: UUID
    drink_id: UUID
    user_id: UserId
    rating: ReviewRating
    comment: str
    created_at: float


class DeleteReviewInputDto(BaseModel):
    review_id: UUID
