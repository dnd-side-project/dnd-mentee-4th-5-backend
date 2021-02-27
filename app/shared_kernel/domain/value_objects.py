import uuid

from pydantic import BaseModel, Field


class UserId(BaseModel):
    value: str = Field(min_length=1, max_length=30)

    def __str__(self):
        return self.value


class UserName(BaseModel):
    value: str = Field(default="", max_length=30)

    def __str__(self):
        return self.value


class DrinkId(BaseModel):
    value: uuid.UUID

    @classmethod
    def build(cls, drink_name: str, created_at: float) -> "DrinkId":
        return cls(value=uuid.uuid5(uuid.NAMESPACE_DNS, name=drink_name + str(created_at)))

    @classmethod
    def from_str(cls, drink_id: str) -> "DrinkId":
        return cls(value=uuid.UUID(drink_id))

    @property
    def uuid(self) -> uuid.UUID:
        return self.value

    def __str__(self):
        return str(self.value)


class ReviewId(BaseModel):
    value: uuid.UUID

    @classmethod
    def build(cls, user_id: str, drink_id: str) -> "ReviewId":
        return cls(value=uuid.uuid5(uuid.NAMESPACE_DNS, name=user_id + drink_id))

    @classmethod
    def from_str(cls, review_id: str) -> "ReviewId":
        return cls(value=uuid.UUID(review_id))

    @property
    def uuid(self) -> uuid.UUID:
        return self.value

    def __str__(self):
        return str(self.value)
