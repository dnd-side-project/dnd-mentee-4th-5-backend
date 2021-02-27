from abc import ABCMeta, abstractmethod
from typing import List, Optional

from pydantic import BaseModel

from wishes.domain.entities import Wish
from wishes.domain.value_objects import WishId


class QueryParam(BaseModel):
    wish_id: Optional[str] = None
    user_id: Optional[str] = None
    drink_id: Optional[str] = None


class WishRepository(metaclass=ABCMeta):
    @abstractmethod
    def find(self, query_param: QueryParam) -> Wish:
        pass

    @abstractmethod
    def find_all(self, query_param: QueryParam) -> List[Wish]:
        pass

    @abstractmethod
    def add(self, wish: Wish) -> None:
        pass

    @abstractmethod
    def delete_by_wish_id(self, wish_id: WishId) -> Wish:
        pass
