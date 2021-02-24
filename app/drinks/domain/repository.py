from abc import ABCMeta, abstractmethod
from typing import List, Optional

from drinks.domain.entities import Drink
from pydantic import BaseModel

from drinks.domain.value_objects import DrinkType, FilterType, OrderType
from shared_kernel.domain.value_objects import DrinkId


class QueryParam(BaseModel):
    type: Optional[DrinkType] = DrinkType.from_str("all")
    filter: Optional[FilterType] = FilterType.from_str("review")
    order: Optional[OrderType] = OrderType.from_str("descending")


class DrinkRepository(metaclass=ABCMeta):
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
