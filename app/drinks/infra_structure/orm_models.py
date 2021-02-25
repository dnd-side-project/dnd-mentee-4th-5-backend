import time

from sqlalchemy import Column, String, Float, Integer, Text
from sqlalchemy.dialects.postgresql import UUID

from drinks.domain.entities import Drink
from drinks.domain.value_objects import DrinkRating, DrinkType
from shared_kernel.domain.value_objects import DrinkId, UserId
from shared_kernel.infra_structure.database import Base


class DrinkOrm(Base):
    __tablename__ = "drink"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(30), nullable=False)
    image_url = Column(Text, default="", nullable=False)
    type = Column(String(30), nullable=False)
    avg_rating = Column(Float, default=0, nullable=False)
    num_of_reviews = Column(Integer, default=0, nullable=False)
    num_of_wish = Column(Integer, default=0, nullable=False)

    @classmethod
    def from_drink(cls, drink: Drink) -> "DrinkOrm":
        return DrinkOrm(
            id=drink.id.uuid,
            name=drink.name,
            image_url=drink.image_url,
            type=str(drink.type),
            avg_rating=float(drink.avg_rating),
            num_of_reviews=drink.num_of_reviews,
            num_of_wish=drink.num_of_wish,
        )

    def fetch_drink(self, drink: Drink) -> None:
        self.id = drink.id.uuid
        self.name = drink.name
        self.image_url = drink.image_url
        self.type = str(drink.type)
        self.avg_rating = float(drink.avg_rating)
        self.num_of_reviews = drink.num_of_reviews
        self.num_of_wish = drink.num_of_wish

    def to_drink(self) -> Drink:
        return Drink(
            id=DrinkId(value=self.id),
            name=self.name,
            image_url=self.image_url,
            type=DrinkType.from_str(self.type),
            avg_rating=DrinkRating(value=self.avg_rating),
            num_of_reviews=self.num_of_reviews,
            num_of_wish=self.num_of_wish,
        )
