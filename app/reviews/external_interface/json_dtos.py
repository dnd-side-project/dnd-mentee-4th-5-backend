from typing import List

from pydantic import BaseModel

from reviews.application.dtos import CreateReviewOutputDto, FindReviewOutputDto, FindReviewsOutputDto


class GetReviewJsonResponse(BaseModel):
    review_id: str
    user_id: str
    drink_id: str
    rating: int
    comment: str
    created_at: float
    updated_at: float

    @classmethod
    def build_by_output_dto(cls, output_dto: FindReviewOutputDto) -> "GetReviewJsonResponse":
        return cls(
            review_id=output_dto.review_id,
            user_id=output_dto.user_id,
            drink_id=output_dto.drink_id,
            rating=output_dto.rating,
            comment=output_dto.comment,
            created_at=output_dto.created_at,
            updated_at=output_dto.updated_at,
        )


class GetReviewsJsonResponse(BaseModel):
    review_id: str
    user_id: str
    drink_id: str
    rating: int
    comment: str
    created_at: float
    updated_at: float

    @classmethod
    def build_by_output_dto(cls, output_dto: FindReviewsOutputDto) -> List["GetReviewsJsonResponse"]:
        return [
            GetReviewsJsonResponse(
                review_id=item.review_id,
                user_id=item.user_id,
                drink_id=item.drink_id,
                rating=item.rating,
                comment=item.comment,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in output_dto.items
        ]


class CreateReviewJsonRequest(BaseModel):
    drink_id: str
    rating: int
    comment: str


class CreateReviewJsonResponse(BaseModel):
    review_id: str
    drink_id: str
    rating: int
    comment: str
    created_at: float
    updated_at: float

    @classmethod
    def build_by_output_dto(cls, output_dto: CreateReviewOutputDto) -> "CreateReviewJsonResponse":
        return cls(
            review_id=output_dto.review_id,
            drink_id=output_dto.drink_id,
            rating=output_dto.rating,
            comment=output_dto.comment,
            created_at=output_dto.created_at,
            updated_at=output_dto.updated_at,
        )


class UpdateReviewJsonRequest(BaseModel):
    review_id: str
    rating: int
    comment: str


class DeleteReviewJsonRequest(BaseModel):
    review_id: str
