from pydantic import BaseModel


class FindDrinkInputDto(BaseModel):
    drink_id: str


class FindDrinkOutputDto(BaseModel):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str
    avg_rating: float
    num_of_reviews: int
    num_of_wish: int


class CreateDrinkInputDto(BaseModel):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str


class UpdateDrinkInputDto(BaseModel):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str
    avg_rating: float
    num_of_reviews: int
    num_of_wish: int


class DeleteDrinkInputDto(BaseModel):
    drink_id: str


class AddDrinkReviewInputDto(BaseModel):
    drink_id: str
    drink_rating: int


class DeleteDrinkReviewInputDto(BaseModel):
    drink_id: str
    drink_rating: int
