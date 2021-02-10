from pydantic import BaseModel, Field


class UserId(BaseModel):
    __root__: str = Field(alias="value", min_length=1, max_length=30)

    def __str__(self):
        return self.__root__


class UserName(BaseModel):
    __root__: str = Field(alias="value", default="", max_length=10)

    def __str__(self):
        return self.__root__
