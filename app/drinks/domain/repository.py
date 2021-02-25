from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union

from pydantic import BaseModel
from drinks.domain.entities import Drink
from drinks.domain.value_objects import DrinkType, FilterType, OrderType
from shared_kernel.domain.value_objects import DrinkId


class QueryParam(BaseModel):
    type: Union[str, DrinkType] = "all"
    filter: Union[str, FilterType] = "review"
    order: Union[str, OrderType] = "descending"

    def to_enum(self) -> "QueryParam":
        self.type = DrinkType.from_str(self.type)
        self.filter = FilterType.from_str(self.filter)
        self.order = OrderType.from_str(self.order)
        return QueryParam(type=self.type, filter=self.filter, order=self.order)

      
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
