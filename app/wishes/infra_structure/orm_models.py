import time

from sqlalchemy import Column, String, Float, Text, BINARY

from shared_kernel.domain.value_objects import UserId, DrinkId
from shared_kernel.infra_structure.database import Base
from wishes.domain.entities import Wish
from wishes.domain.value_objects import WishId


class WishOrm(Base):
    __tablename__ = "wish"

    id = Column(BINARY(16), primary_key=True)
    user_id = Column(String(30), nullable=False)
    drink_id = Column(BINARY(16), nullable=False)
    created_at = Column(Float, default=time.time(), nullable=False)

    @classmethod
    def from_wish(cls, wish: Wish) -> "WishOrm":
        return WishOrm(
            id=wish.id.bytes, user_id=str(wish.user_id), drink_id=wish.drink_id.bytes, created_at=wish.created_at
        )

    def fetch_wish(self, wish: Wish) -> None:
        self.id = wish.id.bytes
        self.user_id = str(wish.user_id)
        self.drink_id = wish.drink_id.bytes
        self.created_at = wish.created_at

    def to_wish(self) -> Wish:
        return Wish(
            id=WishId.from_bytes(self.id),
            user_id=UserId(value=self.user_id),
            drink_id=DrinkId.from_bytes(self.drink_id),
            created_at=self.created_at,
        )
