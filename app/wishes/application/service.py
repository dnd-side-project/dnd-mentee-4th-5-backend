import time
from typing import Union

from shared_kernel.application.dtos import FailedOutputDto
from wishes.application.dto import (
    CreateWishInputDto,
    CreateWishOutputDto,
    DeleteWishInputDto,
    DeleteWishOutputDto,
    FindWishesInputDto,
    FindWishesOutputDto,
)
from wishes.domain.entities import Wish
from wishes.domain.repository import WishRepository, QueryParam
from wishes.domain.value_objects import UserId, DrinkId


class WishApplicationService:
    def __init__(self, wish_repository: WishRepository) -> None:
        self._wish_repository = wish_repository

    def find_wishes(self, input_dto: FindWishesInputDto) -> Union[FindWishesOutputDto, FailedOutputDto]:
        try:
            wishes = self._wish_repository.find_all(input_dto.query_param)
            return FindWishesOutputDto(
                items=[
                    FindWishesOutputDto.Item(
                        user_id=str(wish.user_id), drink_id=str(wish.drink_id), created_at=wish.created_at
                    )
                    for wish in wishes
                ]
            )
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_wish(self, input_dto: CreateWishInputDto) -> Union[CreateWishOutputDto, FailedOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            drink_id = DrinkId.from_str(input_dto.drink_id)
            wish = Wish(user_id=user_id, drink_id=drink_id, created_at=time.time())
            if self._wish_repository.find(QueryParam(user_id=str(user_id), drink_id=str(drink_id))) is not None:
                return FailedOutputDto.build_resource_conflict_error(f"해당 리소스는 이미 존재합니다.")
            self._wish_repository.add(wish)
            return CreateWishOutputDto(user_id=str(user_id), drink_id=str(drink_id), created_at=wish.created_at)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_wish(self, input_dto: DeleteWishInputDto) -> Union[DeleteWishOutputDto, FailedOutputDto]:
        try:
            user_id = UserId(value=input_dto.user_id)
            drink_id = DrinkId.from_str(input_dto.drink_id)
            wish = self._wish_repository.find(QueryParam(user_id=str(user_id), drink_id=str(drink_id)))
            if wish is None:
                return FailedOutputDto.build_resource_not_found_error(f"해당 리소스를 찾지 못했습니다.")
            self._wish_repository.delete(wish)
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
        return DeleteWishOutputDto()
