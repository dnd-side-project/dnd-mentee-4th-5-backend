from typing import List

from pydantic import BaseModel

from wishes.application.dto import CreateWishOutputDto, FindWishesOutputDto


class GetWishesJsonResponse(BaseModel):
    id: str
    user_id: str
    drink_id: str
    created_at: float

    @classmethod
    def build_by_output_dto(cls, output_dto: FindWishesOutputDto) -> List["GetWishesJsonResponse"]:
        return [
            GetWishesJsonResponse(id=item.id, user_id=item.user_id, drink_id=item.user_id, created_at=item.created_at)
            for item in output_dto.items
        ]


class CreateWishJsonResponse(BaseModel):
    user_id: str
    drink_id: str
    created_at: float

    @classmethod
    def build_by_output_dto(cls, output_dto: CreateWishOutputDto) -> "CreateWishJsonResponse":
        return cls(
            user_id=output_dto.user_id,
            drink_id=output_dto.drink_id,
            created_at=output_dto.created_at,
        )


class DeleteWishJsonRequest(BaseModel):
    user_id: str
    drink_id: str
