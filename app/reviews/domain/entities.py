from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic.types import UUID

from reviews.domain.value_objects import ReviewRating, UserId


class Review(BaseModel):
    # uuid5 for test purpose. Use uuid4 later
    MIN_COMMENT_LEN: ClassVar[int] = 0
    MAX_COMMENT_LEN: ClassVar[int] = 300
    id: UUID
    drink_id: UUID
    user_id: UserId
    rating: ReviewRating
    comment: str = Field(min_length=MIN_COMMENT_LEN, max_length=MAX_COMMENT_LEN)
    created_at: float
