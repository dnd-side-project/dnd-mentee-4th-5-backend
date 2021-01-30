from pydantic import BaseModel, Field


class ReviewRating(BaseModel):
    value: int = Field(ge=0, le=5)

