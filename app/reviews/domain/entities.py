from pydantic import BaseModel, Field
from pydantic.types import UUID
from reviews.domain.value_objects import ReviewRating
from users.domain.value_objects import UserId


class Review(BaseModel):
    # uuid5 for test purpose. Use uuid4 later
    id: UUID
    drink_id: UUID
    user_id: UserId
    rating: ReviewRating
    comment: str = Field(min_length=0, max_length=300)
    created_at: float = Field(ge=0)
