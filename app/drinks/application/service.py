import uuid
from typing import Optional, Union

from drinks.application.dtos import (
    AddDrinkReviewInputDto,
    CreateDrinkInputDto,
    DeleteDrinkReviewInputDto,
    FindDrinkInputDto,
    FindDrinkOutputDto,
    UpdateDrinkInputDto,
    DeleteDrinkInputDto,
)
from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository
from drinks.domain.value_objects import DrinkRating
from shared_kernel.application.dtos import FailedOutputDto


class DrinkApplicationService:
    def __init__(self, drink_repository: DrinkRepository) -> None:
        self._drink_repository = drink_repository

    def find_drink(self, input_dto: FindDrinkInputDto) -> Union[FindDrinkOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(drink_id=uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_error(message=f"{str(input_dto.drink_id)}의 술를 찾지 못했습니다.")
            return FindDrinkOutputDto(
                drink_id=str(drink.id),
                drink_name=drink.name,
                drink_image_url=drink.image_url,
                drink_type=drink.type,
                avg_rating=float(drink.avg_rating),
                num_of_reviews=drink.num_of_reviews,
                num_of_wish=drink.num_of_wish,
            )
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_drink(self, input_dto: CreateDrinkInputDto) -> Optional[FailedOutputDto]:
        try:
            drink = Drink(
                id=uuid.UUID(input_dto.drink_id),
                name=input_dto.drink_name,
                image_url=input_dto.drink_image_url,
                type=input_dto.drink_type,
            )

            if self._drink_repository.find_by_drink_id(drink.id) is not None:
                return FailedOutputDto.build_resource_error(f"{str(drink.id)}는 이미 존재하는 술 입니다.")
            self._drink_repository.add(drink)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_drink(self, input_dto: UpdateDrinkInputDto) -> Optional[FailedOutputDto]:
        try:
            drink_id = uuid.UUID(input_dto.drink_id)
            if self._drink_repository.find_by_drink_id(drink_id) is None:
                return FailedOutputDto.build_resource_error(f"{str(drink_id)}의 술을 찾을 수 없습니다.")

            drink = Drink(
                id=drink_id,
                name=input_dto.drink_name,
                image_url=input_dto.drink_image_url,
                type=input_dto.drink_type,
                avg_rating=DrinkRating(value=input_dto.avg_rating),
                num_of_reviews=input_dto.num_of_reviews,
                num_of_wish=input_dto.num_of_wish,
            )
            self._drink_repository.update(drink)

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink(self, input_dto: DeleteDrinkInputDto) -> Optional[FailedOutputDto]:
        try:
            drink_id = uuid.UUID(input_dto.drink_id)
            if self._drink_repository.find_by_drink_id(drink_id) is None:
                return FailedOutputDto.build_resource_error(f"{str(drink_id)}의 술을 찾을 수 없습니다.")

            self._drink_repository.delete_by_drink_id(drink_id)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def add_drink_reviews(self, input_dto: AddDrinkReviewInputDto) -> Optional[FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_error(message=f"{str(input_dto.drink_id)}의 술 찾지 못했습니다.")

            drink.add_review_rating(input_dto.drink_rating)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink_reviews(self, input_dto: DeleteDrinkReviewInputDto) -> Optional[FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_error(message=f"{str(input_dto.drink_id)}의 술을 찾지 못했습니다.")

            drink.delete_review_rating(input_dto.drink_rating)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
