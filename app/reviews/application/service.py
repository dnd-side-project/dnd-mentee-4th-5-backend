from reviews.application.dtos import (
    CreateReviewInputDto,
    DeleteReviewInputDto,
    FindReviewInputDto,
    FindReviewOutputDto,
    UpdateReviewInputDto,
)
from reviews.application.exceptions import ReviewAlreadyExistError, ReviewNotExistError
from reviews.domain.entities import Review
from reviews.domain.repository import ReviewRepository


class ReviewApplicationService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self._user_repository = review_repository

    def find_review(self, input_dto: FindReviewInputDto):
        review = self._user_repository.find_by_review_id(input_dto.review_id)
        if review is None:
            raise ReviewNotExistError(f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다.")

        return FindReviewOutputDto(
            review_id=review.id,
            drink_id=review.drink_id,
            user_id=review.user_id,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at,
        )

    def create_review(self, input_dto: CreateReviewInputDto) -> None:
        if self._user_repository.find_by_review_id(input_dto.review_id) is not None:
            raise ReviewAlreadyExistError(f"{str(input_dto.review_id)}의 리뷰가 이미 존재합니다.")

        review = Review(
            id=input_dto.review_id,
            drink_id=input_dto.drink_id,
            user_id=input_dto.user_id,
            rating=input_dto.rating,
            comment=input_dto.comment,
            created_at=input_dto.created_at,
        )
        self._user_repository.add(review)

    def update_review(self, input_dto: UpdateReviewInputDto) -> None:
        review = self._user_repository.find_by_review_id(input_dto.review_id)
        if review is None:
            raise ReviewNotExistError(f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다.")

        review = Review(
            id=input_dto.review_id,
            drink_id=input_dto.drink_id,
            user_id=input_dto.user_id,
            rating=input_dto.rating,
            comment=input_dto.comment,
            created_at=input_dto.created_at,
        )
        self._user_repository.update(review)

    def delete_review(self, input_dto: DeleteReviewInputDto) -> None:
        review = self._user_repository.find_by_review_id(input_dto.review_id)
        if review is None:
            raise ReviewNotExistError(f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다.")

        self._user_repository.delete_by_review_id(input_dto.review_id)
