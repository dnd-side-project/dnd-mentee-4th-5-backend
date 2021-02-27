from pydantic import BaseModel, Field

from shared_kernel.domain.value_objects import UserId, UserName


class User(BaseModel):
    id: UserId
    name: UserName
    description: str = Field(default="")
    password: str
    image_url: str = Field(default="")
