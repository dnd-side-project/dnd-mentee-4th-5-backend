from typing import ClassVar

from drinks.domain.value_objects import DrinkRating
from pydantic import BaseModel, Field
from pydantic.types import UUID


class Drink(BaseModel):
    MIN_NUM_OF_REVIEWS: ClassVar[int] = 0

    id: UUID
    name: str
    image_url: str
    avg_rating: DrinkRating = Field(default=DrinkRating())
    num_of_reviews: int = Field(default=0, ge=MIN_NUM_OF_REVIEWS)

    def add_review_rating(self, input_rating: int) -> None:
        sum_rating_value = (float(self.avg_rating) * self.num_of_reviews) + input_rating
        self.num_of_reviews = self.num_of_reviews + 1
        self.avg_rating = DrinkRating(value=(sum_rating_value / self.num_of_reviews))

    def delete_review_rating(self, input_rating: int) -> None:
        total_rating_value = (float(self.avg_rating) * self.num_of_reviews) - input_rating
        self.num_of_reviews = self.num_of_reviews - 1

        if self.num_of_reviews == 0:
            self.avg_rating = DrinkRating(value=0)
        else:
            self.avg_rating = DrinkRating(value=(total_rating_value / self.num_of_reviews))
