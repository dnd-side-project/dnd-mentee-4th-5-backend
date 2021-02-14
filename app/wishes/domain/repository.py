from abc import ABCMeta, abstractmethod
from typing import List, Optional

from pydantic import BaseModel
from wishes.domain.entities import Wish


class QueryParam(BaseModel):
    user_id: Optional[str] = None
    drink_id: Optional[str] = None


class WishRepository(metaclass=ABCMeta):
    @abstractmethod
    def find(self, query_param: QueryParam) -> Optional[Wish]:
        pass

    @abstractmethod
    def find_all(self, query_param: QueryParam) -> List[Wish]:
        pass

    @abstractmethod
    def add(self, wish: Wish) -> None:
        pass

    @abstractmethod
    def delete(self, wish: Wish) -> None:
        pass
