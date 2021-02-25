from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union

from pydantic import BaseModel

from reviews.domain.entities import Review
from reviews.domain.value_objects import OrderType
from shared_kernel.domain.value_objects import ReviewId


class QueryParam(BaseModel):
    user_id: Optional[str] = None
    drink_id: Optional[str] = None
    order: Union[str, OrderType] = OrderType.NEWEST

    def to_enum(self) -> "QueryParam":
        self.order = OrderType.from_str(self.order)
        return QueryParam(user_id=self.user_id, drink_id=self.drink_id, order=self.order)


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
