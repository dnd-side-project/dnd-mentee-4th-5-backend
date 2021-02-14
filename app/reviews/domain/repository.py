from abc import ABCMeta, abstractmethod
from typing import List, Optional

from reviews.domain.entities import Review
from reviews.domain.value_objects import DrinkId, OrderType, ReviewId, UserId


class ReviewRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        pass

    @abstractmethod
    def find_all_by_user_id(self, user_id: UserId, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        pass

    @abstractmethod
    def find_all_by_drink_id(self, drink_id: DrinkId, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        pass

    @abstractmethod
    def find_by_review_id(self, review_id: ReviewId) -> Optional[Review]:
        pass

    @abstractmethod
    def find_by_drink_id_user_id(self, drink_id: DrinkId, user_id: UserId) -> Optional[Review]:
        pass

    @abstractmethod
    def add(self, review: Review) -> None:
        pass

    @abstractmethod
    def update(self, review: Review) -> int:
        pass

    @abstractmethod
    def delete_by_review_id(self, review_id: ReviewId) -> None:
        pass
