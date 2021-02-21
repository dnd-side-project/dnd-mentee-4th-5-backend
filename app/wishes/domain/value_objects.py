import uuid

from pydantic import BaseModel, Field


class WishId(BaseModel):
    __root__: uuid.UUID = Field(alias="value")

    @classmethod
    def build(cls, user_id: str, drink_id: str) -> "WishId":
        return cls(value=uuid.uuid5(uuid.NAMESPACE_DNS, name=user_id + drink_id))

    @classmethod
    def from_str(cls, wish_id: str) -> "WishId":
        return cls(value=uuid.UUID(wish_id))

    def __str__(self):
        return str(self.__root__)
