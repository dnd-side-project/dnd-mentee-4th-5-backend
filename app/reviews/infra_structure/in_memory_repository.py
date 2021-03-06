from typing import List, Optional

from reviews.domain.entities import Review
from reviews.domain.repository import ReviewRepository
from reviews.domain.value_objects import OrderType, ReviewRating
from shared_kernel.domain.value_objects import DrinkId, ReviewId, UserId


class InMemoryReviewRepository(ReviewRepository):
    def __init__(self) -> None:
        self.review_id_to_review = {}
        self.drink_id_user_id_to_review_id = {}

    def find_all(self, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        return list(self.review_id_to_review.values())

    def find_all_by_user_id(self, user_id: UserId, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        return [review for review in list(self.review_id_to_review.values()) if review.user_id == user_id]

    def find_all_by_drink_id(self, drink_id: DrinkId, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        return [review for review in list(self.review_id_to_review.values()) if review.drink_id == drink_id]

    def find_by_review_id(self, review_id: ReviewId) -> Optional[Review]:
        return self.review_id_to_review.get(str(review_id), None)

    def find_by_drink_id_user_id(self, drink_id: DrinkId, user_id: UserId):
        review_id = self.drink_id_user_id_to_review_id.get((str(drink_id), str(user_id)), None)
        if not review_id:
            return None
        else:
            return self.review_id_to_review.get(str(review_id), None)

    def add(self, review: Review) -> None:
        self.review_id_to_review[str(review.id)] = review
        self.drink_id_user_id_to_review_id[(str(review.drink_id), str(review.user_id))] = str(review.id)

    def update(self, review: Review) -> ReviewRating:
        old_rating = self.review_id_to_review[str(review.id)].rating
        self.review_id_to_review[str(review.id)] = review
        return old_rating

    def delete_by_review_id(self, review_id: ReviewId) -> None:
        self.review_id_to_review.pop(str(review_id), None)
