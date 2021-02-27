import uuid

from pydantic import BaseModel


class WishId(BaseModel):
    value: uuid.UUID

    @classmethod
    def build(cls, user_id: str, drink_id: str) -> "WishId":
        return cls(value=uuid.uuid5(uuid.NAMESPACE_DNS, name=user_id + drink_id))

    @classmethod
    def from_str(cls, wish_id: str) -> "WishId":
        return cls(value=uuid.UUID(wish_id))

    @property
    def uuid(self) -> uuid.UUID:
        return self.value

    def __str__(self):
        return str(self.value)
