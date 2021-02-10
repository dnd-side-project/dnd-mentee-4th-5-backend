from abc import ABCMeta, abstractmethod
from typing import List, Optional
from uuid import UUID

from reviews.domain.entities import Review
from reviews.domain.value_objects import OrderType, UserId


class ReviewRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        pass

    @abstractmethod
    def find_all_by_user_id(
        self, user_id: UserId, order: OrderType = OrderType.LIKE_DESC
    ) -> List[Review]:
        pass

    @abstractmethod
    def find_all_by_drink_id(
        self, drink_id: UUID, order: OrderType = OrderType.LIKE_DESC
    ) -> List[Review]:
        pass

    @abstractmethod
    def find_by_review_id(self, review_id: UUID) -> Optional[Review]:
        pass

    @abstractmethod
    def find_by_drink_id_user_id(
        self, drink_id: UUID, user_id: UserId
    ) -> Optional[Review]:
        pass

    @abstractmethod
    def add(self, review: Review) -> None:
        pass

    @abstractmethod
    def update(self, review: Review) -> None:
        pass

    @abstractmethod
    def delete_by_review_id(self, review_id: UUID) -> None:
        pass
