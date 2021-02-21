from typing import List

from pydantic import BaseModel

from shared_kernel.application.dtos import SuccessOutputDto
from wishes.domain.repository import QueryParam


class FindWishesInputDto(BaseModel):
    query_param: QueryParam


class FindWishesOutputDto(SuccessOutputDto):
    class Item(BaseModel):
        id: str
        user_id: str
        drink_id: str
        created_at: float

    items: List[Item]


class CreateWishInputDto(BaseModel):
    user_id: str
    drink_id: str


class CreateWishOutputDto(SuccessOutputDto):
    id: str
    user_id: str
    drink_id: str
    created_at: float


class DeleteWishInputDto(BaseModel):
    wish_id: str


class DeleteWishOutputDto(SuccessOutputDto):
    pass
