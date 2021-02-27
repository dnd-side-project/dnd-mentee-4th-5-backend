from typing import List

from pydantic import BaseModel

from drinks.domain.repository import QueryParam
from shared_kernel.application.dtos import SuccessOutputDto


class FindDrinkInputDto(BaseModel):
    drink_id: str


class FindDrinkOutputDto(SuccessOutputDto):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str
    avg_rating: float
    num_of_reviews: int
    num_of_wish: int


class FindDrinksInputDto(BaseModel):
    query_param: QueryParam


class FindDrinksOutputDto(SuccessOutputDto):
    class Item(BaseModel):
        drink_id: str
        drink_name: str
        drink_image_url: str
        drink_type: str
        avg_rating: float
        num_of_reviews: int
        num_of_wish: int

    items: List[Item]


class CreateDrinkInputDto(BaseModel):
    drink_name: str
    drink_image_url: str
    drink_type: str


class CreateDrinkOutputDto(SuccessOutputDto):
    pass


class UpdateDrinkInputDto(BaseModel):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str
    avg_rating: float
    num_of_reviews: int
    num_of_wish: int


class UpdateDrinkOutputDto(SuccessOutputDto):
    pass


class DeleteDrinkInputDto(BaseModel):
    drink_id: str


class DeleteDrinkOutputDto(SuccessOutputDto):
    pass


class AddDrinkReviewInputDto(BaseModel):
    drink_id: str
    drink_rating: int


class AddDrinkReviewOutputDto(SuccessOutputDto):
    pass


class UpdateDrinkReviewInputDto(BaseModel):
    drink_id: str
    old_drink_rating: int
    new_drink_rating: int


class UpdateDrinkReviewOutputDto(SuccessOutputDto):
    pass


class DeleteDrinkReviewInputDto(BaseModel):
    drink_id: str
    drink_rating: int


class DeleteDrinkReviewOutputDto(SuccessOutputDto):
    pass


class AddDrinkWishInputDto(BaseModel):
    drink_id: str


class AddDrinkWishOutputDto(SuccessOutputDto):
    pass


class DeleteDrinkWishInputDto(BaseModel):
    drink_id: str


class DeleteDrinkWishOutputDto(SuccessOutputDto):
    pass
