import uuid
from typing import Optional, Union

from drinks.application.dtos import (AddDrinkReviewInputDto,
                                     AddDrinkReviewOutputDto,
                                     AddDrinkWishInputDto,
                                     AddDrinkWishOutputDto,
                                     CreateDrinkInputDto, CreateDrinkOutputDto,
                                     CreateDrinkWishInputDto,
                                     CreateDrinkWishOutputDto,
                                     DeleteDrinkInputDto, DeleteDrinkOutputDto,
                                     DeleteDrinkReviewInputDto,
                                     DeleteDrinkReviewOutputDto,
                                     DeleteDrinkWishInputDto,
                                     DeleteDrinkWishOutputDto,
                                     FindDrinkInputDto, FindDrinkOutputDto,
                                     FindDrinksInputDto, FindDrinksOutputDto,
                                     UpdateDrinkInputDto, UpdateDrinkOutputDto)
from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository
from drinks.domain.value_objects import (DrinkRating, DrinkType, FilterType,
                                         OrderType)
from shared_kernel.application.dtos import FailedOutputDto


class DrinkApplicationService:
    def __init__(self, drink_repository: DrinkRepository) -> None:
        self._drink_repository = drink_repository

    def find_drink(self, input_dto: FindDrinkInputDto) -> Union[FindDrinkOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(drink_id=uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )
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

    def find_drinks(self, input_dto: FindDrinksInputDto) -> Union[FindDrinksOutputDto, FailedOutputDto]:
        try:
            drink_type = DrinkType.from_str(input_dto.drink_type)
            filter_type = FilterType.from_str(input_dto.filter_type)
            order = OrderType.from_str(input_dto.order)

            drinks = self._drink_repository.find_all(drink_type=drink_type, filter_type=filter_type, order=order)
            drinks_dicts = []
            for drink in drinks:
                temp = {
                    "drink_id": str(drink.id),
                    "drink_name": drink.name,
                    "drink_image_url": drink.image_url,
                    "drink_type": drink.type,
                    # "avg_rating": float(drink.avg_rating),
                    # "num_of_reviews": drink.num_of_reviews,
                    # "num_of_wish": drink.num_of_wish,
                }
                drinks_dicts.append(temp)

            return FindDrinksOutputDto(drinks_dicts=drinks_dicts)

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_drink(self, input_dto: CreateDrinkInputDto) -> Union[CreateDrinkOutputDto, FailedOutputDto]:
        try:
            drink = Drink(
                id=uuid.UUID(input_dto.drink_id),
                name=input_dto.drink_name,
                image_url=input_dto.drink_image_url,
                type=DrinkType.from_str(input_dto.drink_type),
            )

            if self._drink_repository.find_by_drink_id(drink.id) is not None:
                return FailedOutputDto.build_resource_conflict_error(f"{str(drink.id)}는 이미 존재하는 술 입니다.")
            self._drink_repository.add(drink)
            return CreateDrinkOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_drink(self, input_dto: UpdateDrinkInputDto) -> Union[UpdateDrinkOutputDto, FailedOutputDto]:
        try:
            drink_id = uuid.UUID(input_dto.drink_id)
            if self._drink_repository.find_by_drink_id(drink_id) is None:
                return FailedOutputDto.build_resource_not_found_error(f"{str(drink_id)}의 술을 찾을 수 없습니다.")

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
            return UpdateDrinkOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink(self, input_dto: DeleteDrinkInputDto) -> Union[DeleteDrinkOutputDto, FailedOutputDto]:
        try:
            drink_id = uuid.UUID(input_dto.drink_id)
            if self._drink_repository.find_by_drink_id(drink_id) is None:
                return FailedOutputDto.build_resource_not_found_error(f"{str(drink_id)}의 술을 찾을 수 없습니다.")

            self._drink_repository.delete_by_drink_id(drink_id)
            return DeleteDrinkOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def add_drink_review(self, input_dto: AddDrinkReviewInputDto) -> Union[AddDrinkReviewOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )

            drink.add_rating(input_dto.drink_rating)
            return AddDrinkReviewOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink_review(
        self, input_dto: DeleteDrinkReviewInputDto
    ) -> Union[DeleteDrinkReviewOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )

            drink.delete_rating(input_dto.drink_rating)
            return DeleteDrinkReviewOutputDto()

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def add_drink_wish(self, input_dto: AddDrinkWishInputDto) -> Union[AddDrinkWishOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )
            drink.add_wish()
            return AddDrinkWishOutputDto()
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink_wish(
        self, input_dto: DeleteDrinkWishInputDto
    ) -> Union[DeleteDrinkWishOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(uuid.UUID(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )
            drink.delete_wish()
            return DeleteDrinkWishOutputDto()
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
