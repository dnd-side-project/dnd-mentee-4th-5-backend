import uuid

from pydantic import BaseModel, Field


class UserId(BaseModel):
    __root__: str = Field(alias="value", min_length=1, max_length=30)

    def __str__(self):
        return self.__root__


class DrinkId(BaseModel):
    __root__: uuid.UUID = Field(alias="value")

    @classmethod
    def from_str(cls, drink_id: str) -> "DrinkId":
        return cls(value=uuid.UUID(drink_id))

    def __str__(self):
        return str(self.__root__)
