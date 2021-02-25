from pydantic import BaseModel

from drinks.application.dtos import FindDrinkOutputDto


class CreateDrinkJsonRequest(BaseModel):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str


class GetDrinksJsonRequest(BaseModel):
    drink_type: str
    filter_type: str
    order: str


class GetDrinkJsonResponse(BaseModel):
    drink_id: str
    name: str
    image_url: str
    type: str
    avg_rating: float
    num_of_reviews: int
    num_of_wish: int

    @classmethod
    def build_by_output_dto(cls, output_dto: FindDrinkOutputDto) -> "GetDrinkJsonResponse":
        return cls(
            drink_id=output_dto.drink_id,
            name=output_dto.drink_name,
            image_url=output_dto.drink_image_url,
            type=output_dto.drink_type,
            avg_rating=output_dto.avg_rating,
            num_of_reviews=output_dto.num_of_reviews,
            num_of_wish=output_dto.num_of_wish,
        )
