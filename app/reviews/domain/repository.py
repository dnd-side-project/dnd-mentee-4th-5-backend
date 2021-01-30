from abc import ABCMeta, abstractmethod
from typing import List, Optional
from uuid import UUID

from reviews.domain.entities import Review


class ReviewRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> List[Review]:
        pass

    @abstractmethod
    def find_by_review_id(self, review_id: UUID) -> Optional[Review]:
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
