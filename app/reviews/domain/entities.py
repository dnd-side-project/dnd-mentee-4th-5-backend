import uuid
from datetime import datetime

from pydantic import BaseModel, Field
from reviews.domain.value_objects import ReviewRating


class Review(BaseModel):
    # uuid5 for test purpose. Use uuid4 later
    id: uuid.UUID
    drink_id: uuid.UUID
    user_id: UserId
    rating: ReviewRating
    comment: Field(str, min_length=0, max_length=300)
    created_at: datetime