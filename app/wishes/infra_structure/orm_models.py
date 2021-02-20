import time

from sqlalchemy import Column, String, Float

from shared_kernel.domain.value_objects import UserId, DrinkId
from shared_kernel.infra_structure.database import Base
from wishes.domain.entities import Wish
from wishes.domain.value_objects import WishId


class WishOrm(Base):
    __tablename__ = "wish"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    drink_id = Column(String, nullable=False)
    created_at = Column(Float, default=time.time(), nullable=False)

    @classmethod
    def from_wish(cls, wish: Wish) -> "WishOrm":
        return WishOrm(
            id=str(wish.id), user_id=str(wish.user_id), drink_id=str(wish.drink_id), created_at=wish.created_at
        )

    def fetch_wish(self, wish: Wish) -> None:
        self.id = str(wish)
        self.user_id = str(wish.user_id)
        self.drink_id = str(wish.drink_id)
        self.created_at = wish.created_at

    def to_wish(self) -> Wish:
        return Wish(
            id=WishId.from_str(self.id),
            user_id=UserId(value=self.user_id),
            drink_id=DrinkId.from_str(self.drink_id),
            created_at=self.created_at,
        )
