from typing import List

from pydantic import BaseModel, Field
from wishes.application.dto import CreateWishOutputDto, FindWishesOutputDto


class GetWishesJsonResponse(BaseModel):
    __root__: List[FindWishesOutputDto.Item] = Field(alias="value")


class CreateWishJsonResponse(BaseModel):
    user_id: str
    drink_id: str
    created_at: float

    @classmethod
    def build_by_output_dto(
        cls, output_dto: CreateWishOutputDto
    ) -> "CreateWishJsonResponse":
        return cls(
            user_id=output_dto.user_id,
            drink_id=output_dto.drink_id,
            created_at=output_dto.created_at,
        )


class DeleteWishJsonRequest(BaseModel):
    user_id: str
    drink_id: str
