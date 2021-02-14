import json

from drinks.application.dtos import FindDrinksOutputDto
from pydantic import BaseModel


class CreateDrinkJsonRequest(BaseModel):
    drink_id: str
    drink_name: str
    drink_image_url: str
    drink_type: str


class GetDrinksJsonRequest(BaseModel):
    drink_type: str
    filter_type: str
    order: str


class GetDrinksJsonResponse(BaseModel):
    drinks_json: str

    @classmethod
    def build_by_output_dto(
        cls, output_dto: FindDrinksOutputDto
    ) -> "GetDrinksJsonResponse":
        return cls(drinks_json=json.dumps(output_dto.drinks_dicts))
