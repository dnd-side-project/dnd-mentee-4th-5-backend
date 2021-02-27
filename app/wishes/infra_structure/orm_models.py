import time

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

from shared_kernel.domain.value_objects import UserId, DrinkId
from shared_kernel.infra_structure.database import Base
from wishes.domain.entities import Wish
from wishes.domain.value_objects import WishId


class WishOrm(Base):
    __tablename__ = "wish"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String(30), nullable=False)
    drink_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(Float, default=time.time(), nullable=False)

    @classmethod
    def from_wish(cls, wish: Wish) -> "WishOrm":
        return WishOrm(
            id=wish.id.uuid, user_id=str(wish.user_id), drink_id=wish.drink_id.uuid, created_at=wish.created_at
        )

    def fetch_wish(self, wish: Wish) -> None:
        self.id = wish.id.uuid
        self.user_id = str(wish.user_id)
        self.drink_id = wish.drink_id.uuid
        self.created_at = wish.created_at

    def to_wish(self) -> Wish:
        return Wish(
            id=WishId(value=self.id),
            user_id=UserId(value=self.user_id),
            drink_id=DrinkId(value=self.drink_id),
            created_at=self.created_at,
        )
