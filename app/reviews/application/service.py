import time
from typing import Union

from drinks.application.dtos import AddDrinkReviewInputDto, DeleteDrinkReviewInputDto, UpdateDrinkReviewInputDto
from drinks.application.service import DrinkApplicationService
from reviews.application.dtos import (
    CreateReviewInputDto,
    CreateReviewOutputDto,
    DeleteReviewInputDto,
    DeleteReviewOutputDto,
    FindReviewInputDto,
    FindReviewOutputDto,
    FindReviewsInputDto,
    FindReviewsOutputDto,
    UpdateReviewInputDto,
    UpdateReviewOutputDto,
)
from reviews.domain.entities import Review
from reviews.domain.repository import ReviewRepository
from reviews.domain.value_objects import ReviewRating
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import InvalidParamInputError, ResourceAlreadyExistError, ResourceNotFoundError
from shared_kernel.domain.value_objects import ReviewId, DrinkId, UserId


class ReviewApplicationService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self._review_repository = review_repository

    def find_review(self, input_dto: FindReviewInputDto) -> Union[FindReviewOutputDto, FailedOutputDto]:
        try:
            review_id = ReviewId.from_str(input_dto.review_id)
            review = self._review_repository.find_by_review_id(review_id)
            return FindReviewOutputDto(
                review_id=str(review.id),
                drink_id=str(review.drink_id),
                user_id=str(review.user_id),
                rating=int(review.rating),
                comment=review.comment,
                created_at=review.created_at,
                updated_at=review.updated_at,
            )
        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def find_reviews(self, input_dto: FindReviewsInputDto) -> Union[FailedOutputDto, FindReviewsOutputDto]:
        try:
            reviews = self._review_repository.find_all(query_param=input_dto.query_param)
            return FindReviewsOutputDto(
                items=[
                    FindReviewsOutputDto.Item(
                        review_id=str(review.id),
                        drink_id=str(review.drink_id),
                        user_id=str(review.user_id),
                        rating=int(review.rating),
                        comment=review.comment,
                        created_at=review.created_at,
                        updated_at=review.updated_at,
                    )
                    for review in reviews
                ]
            )
        except InvalidParamInputError as e:
            return FailedOutputDto.build_parameters_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_review(
        self,
        input_dto: CreateReviewInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[CreateReviewOutputDto, FailedOutputDto]:
        try:
            review = Review(
                id=ReviewId.build(user_id=input_dto.user_id, drink_id=input_dto.drink_id),
                drink_id=DrinkId(value=input_dto.drink_id),
                user_id=UserId(value=input_dto.user_id),
                rating=ReviewRating(value=input_dto.rating),
                comment=input_dto.comment,
                created_at=time.time(),
                updated_at=time.time(),
            )
            self._review_repository.add(review)
            input_dto = AddDrinkReviewInputDto(drink_id=input_dto.drink_id, drink_rating=input_dto.rating)
            drink_add_review_output_dto = drink_application_service.add_drink_review(input_dto=input_dto)

            if not drink_add_review_output_dto.status:
                return drink_add_review_output_dto
            return CreateReviewOutputDto(
                review_id=str(review.id),
                drink_id=str(review.drink_id),
                user_id=str(review.user_id),
                rating=int(review.rating),
                comment=review.comment,
                created_at=review.created_at,
                updated_at=review.updated_at,
            )
        except ResourceAlreadyExistError as e:
            return FailedOutputDto.build_resource_conflict_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_review(
        self,
        input_dto: UpdateReviewInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[UpdateReviewOutputDto, FailedOutputDto]:
        try:
            review_id = ReviewId.from_str(input_dto.review_id)
            old_review = self._review_repository.find_by_review_id(review_id)

            old_rating = int(old_review.rating)

            new_review = Review(
                id=old_review.id,
                drink_id=old_review.drink_id,
                user_id=old_review.user_id,
                rating=ReviewRating(value=input_dto.rating),
                comment=input_dto.comment,
                created_at=old_review.created_at,
                updated_at=time.time(),
            )
            self._review_repository.update(new_review)

            drinks_input_dto = UpdateDrinkReviewInputDto(
                drink_id=str(new_review.drink_id),
                old_drink_rating=old_rating,
                new_drink_rating=input_dto.rating,
            )
            drink_update_review_output_dto = drink_application_service.update_drink_review(input_dto=drinks_input_dto)

            if not drink_update_review_output_dto.status:
                return drink_update_review_output_dto
            return UpdateReviewOutputDto()
        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
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
                return FailedOutputDto.build_resource_not_found_error(f"{str(input_dto.review_id)}의 리뷰를 찾을 수 없습니다.")

            self._review_repository.delete_by_review_id(review_id)
            drinks_input_dto = DeleteDrinkReviewInputDto(
                drink_id=str(review.drink_id), drink_rating=int(review.rating)
            )
            drink_delete_review_output_dto = drink_application_service.delete_drink_review(input_dto=drinks_input_dto)

            if not drink_delete_review_output_dto.status:
                return drink_delete_review_output_dto
            return DeleteReviewOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
