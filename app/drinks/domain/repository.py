from abc import ABCMeta, abstractmethod
from typing import List, Optional

from drinks.domain.entities import Drink
from drinks.domain.value_objects import DrinkId
from pydantic import BaseModel


class QueryParam(BaseModel):
    drink: Optional[str] = "all"
    filter: Optional[str] = "review"
    order: Optional[str] = "descending"


class DrinkRepository(metaclass=ABCMeta):
    # test use only
    @abstractmethod
    def find_all_simple(self) -> List[Drink]:
        pass

    @abstractmethod
    def find_all(self, query_param: QueryParam) -> List[Drink]:
        pass

    @abstractmethod
    def find_by_drink_id(self, drink_id: DrinkId) -> Optional[Drink]:
        pass

    @abstractmethod
    def add(self, drink: Drink) -> None:
        pass

    @abstractmethod
    def update(self, drink: Drink) -> None:
        pass

    @abstractmethod
    def delete_by_drink_id(self, drink_id: DrinkId) -> None:
        pass
