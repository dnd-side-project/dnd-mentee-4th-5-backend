from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class DrinkRating(BaseModel):
    MIN_VALUE: ClassVar[int] = 0.0
    MAX_VALUE: ClassVar[int] = 5.0
    __root__: float = Field(alias="value", default=0.0, ge=MIN_VALUE, le=MAX_VALUE)

    def __float__(self) -> float:
        return self.__root__


class DrinkType(str, Enum):
    ALL = "ALL"
    BEER = "BEER"
    WINE = "WINE"
    LIQUOR = "LIQUOR"
    SAKE = "SAKE"
    SOJU = "SOJU"
    ETC = "ETC"


class FilterType(str, Enum):
    RATING = "RATING"
    REVIEW = "REVIEW"
    WISH = "WISH"


class OrderType(str, Enum):
    DESC = "DESC"
    ASC = "ASC"
