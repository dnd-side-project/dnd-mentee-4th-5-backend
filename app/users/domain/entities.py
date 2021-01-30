from typing import List

from pydantic import BaseModel, Field
from users.domain.value_objects import UserId, UserName


class User(BaseModel):
    id: UserId
    name: UserName
    description: str = Field(default="")
    hashed_password: str
    image_url: str = Field(default="")
    review_ids: List[str] = Field(default=[])
    wished_drinks_ids: List[str] = Field(default=[])
