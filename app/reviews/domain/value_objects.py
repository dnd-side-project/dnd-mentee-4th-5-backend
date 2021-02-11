import uuid
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class ReviewId(BaseModel):
    __root__: uuid.UUID = Field(alias="value")

    @classmethod
    def build(cls, user_id: str, drink_id: str) -> "ReviewId":
        return cls(value=uuid.uuid5(uuid.NAMESPACE_DNS, name=user_id + drink_id))

    @classmethod
    def from_str(cls, review_id: str) -> "ReviewId":
        return cls(value=uuid.UUID(review_id))

    def __str__(self):
        return str(self.__root__)


class ReviewRating(BaseModel):
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 5
    __root__: int = Field(alias="value", ge=MIN_VALUE, le=MAX_VALUE)

    def __int__(self):
        return self.__root__


class OrderType(Enum):
    LIKE_DESC = "like_desc"
    LIKE_ASC = "like_asc"
    NEWEST = "newest"


class UserId(BaseModel):
    __root__: str = Field(alias="value", min_length=1, max_length=30)

    def __str__(self):
        return self.__root__


class DrinkId(BaseModel):
    __root__: uuid.UUID = Field(alias="value")

    @classmethod
    def from_str(cls, drink_id: str) -> "DrinkId":
        return cls(value=uuid.UUID(drink_id))

    def __str__(self):
        return str(self.__root__)
