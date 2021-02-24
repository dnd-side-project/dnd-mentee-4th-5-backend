from abc import ABCMeta, abstractmethod
from typing import List, Optional

from pydantic import BaseModel
from reviews.domain.entities import Review
from reviews.domain.value_objects import OrderType
from shared_kernel.domain.value_objects import DrinkId, ReviewId, UserId


class QueryParam(BaseModel):
    userId: Optional[str] = None
    drinkId: Optional[str] = None
    order: OrderType = OrderType.NEWEST


class ReviewRepository(metaclass=ABCMeta):
    @abstractmethod
    def find(self, query_param: QueryParam) -> Review:
        pass

    @abstractmethod
    def find_all(self, query_param: QueryParam) -> List[Review]:
        pass

    @abstractmethod
    def find_by_review_id(self, review_id: ReviewId) -> Optional[Review]:
        pass

    @abstractmethod
    def add(self, review: Review) -> None:
        pass

    @abstractmethod
    def update(self, review: Review) -> None:
        pass

    @abstractmethod
    def delete_by_review_id(self, review_id: ReviewId) -> None:
        pass
