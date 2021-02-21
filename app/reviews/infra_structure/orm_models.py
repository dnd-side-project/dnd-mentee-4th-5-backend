import time

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from reviews.domain.entities import Review
from reviews.domain.value_objects import ReviewRating
from shared_kernel.domain.value_objects import UserId, DrinkId, ReviewId
from shared_kernel.infra_structure.database import Base


class ReviewOrm(Base):
    __tablename__ = "review"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String(30), nullable=False)
    drink_id = Column(UUID(as_uuid=True), nullable=False)
    rating: Column(Integer, nullable=False)
    comment: Column(String(300), default="", nullable=False)
    created_at: Column(Float, default=time.time(), nullable=False)
    updated_at: Column(Float, default=time.time(), nullable=False)

    @classmethod
    def from_review(cls, review: Review) -> "ReviewOrm":
        return ReviewOrm(
            id=review.id.,
            user_id=str(review.user_id),
            drink_id=review.drink_id,
            rating=int(review.rating),
            comment=review.comment,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    def fetch_review(self, review: Review) -> None:
        self.id = review
        self.user_id = str(review.user_id)
        self.drink_id = review.drink_id
        self.rating = int(review.rating)
        self.comment = review.comment
        self.created_at = review.created_at
        self.updated_at = review.updated_at

    def to_review(self) -> Review:
        return Review(
            id=ReviewId(value=self.id),
            user_id=UserId(value=self.user_id),
            drink_id=DrinkId(value=self.drink_id),
            rating=ReviewRating(value=self.rating),
            comment=self.comment,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
