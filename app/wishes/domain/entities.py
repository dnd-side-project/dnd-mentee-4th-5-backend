from pydantic import BaseModel
from wishes.domain.value_objects import DrinkId, UserId


class Wish(BaseModel):
    user_id: UserId
    drink_id: DrinkId
    created_at: float
