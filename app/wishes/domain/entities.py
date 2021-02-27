from pydantic import BaseModel

from shared_kernel.domain.value_objects import UserId, DrinkId
from wishes.domain.value_objects import WishId


class Wish(BaseModel):
    id: WishId
    user_id: UserId
    drink_id: DrinkId
    created_at: float
