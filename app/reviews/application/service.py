import time
from typing import Union

from drinks.application.dtos import (AddDrinkReviewInputDto,
                                     DeleteDrinkReviewInputDto,
                                     UpdateDrinkReviewInputDto)
from drinks.application.service import DrinkApplicationService
from reviews.application.dtos import (CreateReviewInputDto,
                                      CreateReviewOutputDto,
                                      DeleteReviewInputDto,
                                      DeleteReviewOutputDto,
                                      FindReviewInputDto, FindReviewOutputDto,
                                      FindReviewsByDrinkIdInputDto,
                                      FindReviewsByDrinkIdOutputDto,
                                      FindReviewsByUserIdInputDto,
                                      FindReviewsByUserIdOutputDto,
                                      UpdateReviewInputDto,
                                      UpdateReviewOutputDto)
from reviews.domain.entities import Review
from reviews.domain.repository import ReviewRepository
from reviews.domain.value_objects import (DrinkId, ReviewId, ReviewRating,
                                          UserId)
from shared_kernel.application.dtos import FailedOutputDto


class ReviewApplicationService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self._review_repository = review_repository

    def find_review(
        self, input_dto: FindReviewInputDto
    ) -> Union[FindReviewOutputDto, FailedOutputDto]:
        try:
            review_id = ReviewId.from_str(input_dto.review_id)
            review = self._review_repository.find_by_review_id(review_id)
            if review is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다."
                )
            return FindReviewOutputDto(
                review_id=str(review.id),
                drink_id=str(review.drink_id),
                user_id=str(review.user_id),
                rating=int(review.rating),
                comment=review.comment,
                created_at=review.created_at,
                updated_at=review.updated_at,
            )

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    # def find_reviews(self, input_dto: FindReviewsInputDto) -> Union[FindReviewsOutputDto, FailedOutputDto]:
    #     try:
    #
    #     except Exception as e:
    #         return FailedOutputDto.build_system_error(message=str(e))

    def create_review(
        self,
        input_dto: CreateReviewInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[CreateReviewOutputDto, FailedOutputDto]:
        try:
            drink_id = DrinkId.from_str(input_dto.drink_id)
            user_id = UserId(value=input_dto.user_id)
            if (
                self._review_repository.find_by_drink_id_user_id(drink_id, user_id)
                is not None
            ):
                return FailedOutputDto.build_resource_conflict_error(
                    f"user: {str(user_id)}, drink: {str(drink_id)} 의 리뷰가 이미 존재합니다."
                )
            review = Review(
                id=ReviewId.build(user_id=str(user_id), drink_id=str(drink_id)),
                drink_id=drink_id,
                user_id=user_id,
                rating=ReviewRating(value=input_dto.rating),
                comment=input_dto.comment,
                created_at=time.time(),
                updated_at=time.time(),
            )
            self._review_repository.add(review)
            input_dto = AddDrinkReviewInputDto(
                drink_id=input_dto.drink_id, drink_rating=input_dto.rating
            )
            drink_add_review_output_dto = drink_application_service.add_drink_review(
                input_dto=input_dto
            )

            if not drink_add_review_output_dto.status:
                return drink_add_review_output_dto
            return CreateReviewOutputDto(
                drink_id=str(review.drink_id),
                user_id=str(review.user_id),
                rating=int(review.rating),
                comment=review.comment,
                created_at=review.created_at,
                updated_at=review.updated_at,
            )

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_review(
        self,
        input_dto: UpdateReviewInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[UpdateReviewOutputDto, FailedOutputDto]:
        try:
            review_id = ReviewId.from_str(input_dto.review_id)
            review = self._review_repository.find_by_review_id(review_id)
            if review is None:
                return FailedOutputDto.build_resource_not_found_error(
                    f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다."
                )
            old_rating = int(review.rating)

            review = Review(
                id=review.id,
                drink_id=review.drink_id,
                user_id=review.user_id,
                rating=ReviewRating(value=input_dto.rating),
                comment=input_dto.comment,
                created_at=review.created_at,
                updated_at=time.time(),
            )
            self._review_repository.update(review)

            drinks_input_dto = UpdateDrinkReviewInputDto(
                drink_id=str(review.drink_id),
                old_drink_rating=old_rating,
                new_drink_rating=input_dto.rating,
            )
            drink_update_review_output_dto = (
                drink_application_service.update_drink_review(
                    input_dto=drinks_input_dto
                )
            )

            if not drink_update_review_output_dto.status:
                return drink_update_review_output_dto
            return UpdateReviewOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_review(
        self,
        input_dto: DeleteReviewInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[DeleteReviewOutputDto, FailedOutputDto]:
        try:
            review_id = ReviewId.from_str(input_dto.review_id)
            review = self._review_repository.find_by_review_id(review_id)
            if review is None:
                return FailedOutputDto.build_resource_not_found_error(
                    f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다."
                )

            self._review_repository.delete_by_review_id(review_id)
            drinks_input_dto = DeleteDrinkReviewInputDto(
                drink_id=str(review.drink_id), drink_rating=int(review.rating)
            )
            drink_delete_review_output_dto = (
                drink_application_service.delete_drink_review(
                    input_dto=drinks_input_dto
                )
            )

            if not drink_delete_review_output_dto.status:
                return drink_delete_review_output_dto
            return DeleteReviewOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def find_reviews_by_user_id(
        self, input_dto: FindReviewsByUserIdInputDto
    ) -> Union[FailedOutputDto, FindReviewsByUserIdOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            reviews = self._review_repository.find_all_by_user_id(user_id)
            reviews_dicts = [review.dict() for review in reviews]
            return FindReviewsByUserIdOutputDto(reviews_dicts=reviews_dicts)

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def find_reviews_by_drink_id(
        self, input_dto: FindReviewsByDrinkIdInputDto
    ) -> Union[FailedOutputDto, FindReviewsByDrinkIdOutputDto]:
        try:
            drink_id = DrinkId.from_str(input_dto.drink_id)
            reviews = self._review_repository.find_all_by_drink_id(drink_id)
            reviews_dicts = [review.dict() for review in reviews]
            return FindReviewsByDrinkIdOutputDto(reviews_dicts=reviews_dicts)

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
