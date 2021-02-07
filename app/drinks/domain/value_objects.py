from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class DrinkRating(BaseModel):
    MIN_VALUE: ClassVar[int] = 0
    MAX_VALUE: ClassVar[int] = 5
    __root__: float = Field(alias="value", default=0, ge=MIN_VALUE, le=MAX_VALUE)

    def __float__(self) -> float:
        return self.__root__


class OrderType(Enum):
    REVIEW_NUM_DESC = "reviews_num_desc"
    REVIEW_NUM_ASC = "reviews_num_asc"
