from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class ReviewRating(BaseModel):
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 5
    value: int = Field(ge=MIN_VALUE, le=MAX_VALUE)

    def __int__(self):
        return self.value


class OrderType(Enum):
    LIKE_DESC = "like_desc"
    LIKE_ASC = "like_asc"
    NEWEST = "newest"
