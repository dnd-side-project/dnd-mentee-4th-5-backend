from typing import ClassVar
from uuid import UUID

from drinks.domain.value_objects import DrinkRating, DrinkType
from pydantic import BaseModel, Field


class Drink(BaseModel):
    MIN_NUM_OF_REVIEWS: ClassVar[int] = 0
    MIN_NUM_OF_WISH: ClassVar[int] = 0

    id: UUID
    name: str
    image_url: str
    type: DrinkType
    avg_rating: DrinkRating = Field(default=DrinkRating())
    num_of_reviews: int = Field(default=0, ge=MIN_NUM_OF_REVIEWS)
    num_of_wish: int = Field(default=0, ge=MIN_NUM_OF_WISH)

    def add_review_rating(self, input_rating: int) -> None:
        sum_rating_value = (float(self.avg_rating) * self.num_of_reviews) + input_rating
        self.num_of_reviews += 1
        self.avg_rating = DrinkRating(value=(sum_rating_value / self.num_of_reviews))

    def delete_review_rating(self, input_rating: int) -> None:
        total_rating_value = (float(self.avg_rating) * self.num_of_reviews) - input_rating
        self.num_of_reviews -= 1

        if self.num_of_reviews == 0:
            self.avg_rating = DrinkRating(value=0)
        else:
            self.avg_rating = DrinkRating(value=(total_rating_value / self.num_of_reviews))

    def add_user_wish_list(self) -> None:
        self.num_of_wish += 1
