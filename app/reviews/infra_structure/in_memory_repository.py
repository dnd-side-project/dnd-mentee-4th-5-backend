from typing import List, Optional
from uuid import UUID

from reviews.domain.entities import Review
from reviews.domain.repository import ReviewRepository


class InMemoryReviewRepository(ReviewRepository):
    def __init__(self) -> None:
        self.review_id_to_review = {}

    def find_by_review_id(self, review_id: UUID) -> Optional[Review]:
        return self.review_id_to_review.get(str(review_id), None)

    def add(self, review: Review) -> None:
        self.review_id_to_review[str(review.id)] = review

    def update(self, review: Review) -> None:
        self.review_id_to_review[str(review.id)] = review

    def find_all(self) -> List[Review]:
        return list(self.review_id_to_review.values())

    def delete_by_review_id(self, review_id: UUID) -> None:
        self.review_id_to_review.pop(str(review_id), None)
