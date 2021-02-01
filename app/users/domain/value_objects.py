from pydantic import BaseModel, Field


class UserId(BaseModel):
    value: str = Field(min_length=1, max_length=30)

    def __str__(self):
        return self.value


class UserName(BaseModel):
    value: str = Field(default="", max_length=10)

    def __str__(self):
        return self.value
