from abc import ABCMeta, abstractmethod
from typing import List, Optional

from pydantic import BaseModel
from reviews.domain.entities import Review
from reviews.domain.value_objects import DrinkId, OrderType, ReviewId, UserId


class QueryParam(BaseModel):
    user_id: Optional[str] = None
    drink_id: Optional[str] = None


class ReviewRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self, query_param: QueryParam, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        pass

    @abstractmethod
    def find_by_review_id(self, review_id: ReviewId) -> Optional[Review]:
        pass

    @abstractmethod
    def find_by_drink_id_user_id(
        self,
        query_param: QueryParam,
    ) -> Optional[Review]:
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
