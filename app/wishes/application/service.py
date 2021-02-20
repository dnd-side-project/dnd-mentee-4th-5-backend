import time
from typing import Union

from drinks.application.dtos import AddDrinkWishInputDto, DeleteDrinkWishInputDto
from drinks.application.service import DrinkApplicationService
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from shared_kernel.domain.value_objects import UserId, DrinkId
from wishes.application.dto import (
    CreateWishInputDto,
    CreateWishOutputDto,
    DeleteWishInputDto,
    DeleteWishOutputDto,
    FindWishesInputDto,
    FindWishesOutputDto,
)
from wishes.domain.entities import Wish
from wishes.domain.repository import WishRepository
from wishes.domain.value_objects import WishId


class WishApplicationService:
    def __init__(self, wish_repository: WishRepository) -> None:
        self._wish_repository = wish_repository

    def find_wishes(self, input_dto: FindWishesInputDto) -> Union[FindWishesOutputDto, FailedOutputDto]:
        try:
            wishes = self._wish_repository.find_all(input_dto.query_param)
            return FindWishesOutputDto(
                items=[
                    FindWishesOutputDto.Item(
                        id=str(wish.id),
                        user_id=str(wish.user_id),
                        drink_id=str(wish.drink_id),
                        created_at=wish.created_at,
                    )
                    for wish in wishes
                ]
            )
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_wish(
        self,
        input_dto: CreateWishInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[CreateWishOutputDto, FailedOutputDto]:
        try:
            wish = Wish(
                id=WishId.build(user_id=str(input_dto.user_id), drink_id=str(input_dto.drink_id)),
                user_id=UserId(value=input_dto.user_id),
                drink_id=DrinkId.from_str(input_dto.drink_id),
                created_at=time.time(),
            )
            self._wish_repository.add(wish)

            add_drink_wish_input_dto = AddDrinkWishInputDto(drink_id=input_dto.drink_id)
            add_drink_wish_output_dto = drink_application_service.add_drink_wish(input_dto=add_drink_wish_input_dto)

            if not add_drink_wish_output_dto.status:
                return add_drink_wish_output_dto
            return CreateWishOutputDto(
                id=str(wish.id), user_id=str(wish.user_id), drink_id=str(wish.drink_id), created_at=wish.created_at
            )
        except ResourceAlreadyExistError as e:
            return FailedOutputDto.build_resource_conflict_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_wish(
        self,
        input_dto: DeleteWishInputDto,
        drink_application_service: DrinkApplicationService,
    ) -> Union[DeleteWishOutputDto, FailedOutputDto]:
        try:
            wish = self._wish_repository.delete_by_wish_id(WishId.from_str(input_dto.wish_id))

            delete_drink_wish_input_dto = DeleteDrinkWishInputDto(drink_id=str(wish.drink_id))
            delete_drink_wish_output_dto = drink_application_service.delete_drink_wish(
                input_dto=delete_drink_wish_input_dto
            )

            if not delete_drink_wish_output_dto.status:
                return delete_drink_wish_output_dto
            return DeleteWishOutputDto()
        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
