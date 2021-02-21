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
    ALL = "all"
    BEER = "beer"
    WINE = "wine"
    LIQUOR = "liquor"
    SAKE = "sake"
    SOJU = "soju"
    ETC = "etc"

    @staticmethod
    def from_str(label):
        switcher = {
            "all": DrinkType.ALL,
            "beer": DrinkType.BEER,
            "wine": DrinkType.WINE,
            "liquor": DrinkType.LIQUOR,
            "sake": DrinkType.SAKE,
            "soju": DrinkType.SOJU,
            "etc": DrinkType.ETC,
        }
        return switcher.get(label, DrinkType.ALL)


class FilterType(str, Enum):
    REVIEW = "review"
    RATING = "rating"
    WISH = "wish"

    @staticmethod
    def from_str(label):
        switcher = {
            "review": FilterType.REVIEW,
            "rating": FilterType.RATING,
            "wish": FilterType.WISH,
        }
        return switcher.get(label, FilterType.REVIEW)


class OrderType(str, Enum):
    DESC = "descending"
    ASC = "ascending"

    @staticmethod
    def from_str(label):
        switcher = {
            "descending": OrderType.DESC,
            "ascending": OrderType.ASC,
        }
        return switcher.get(label, OrderType.DESC)
