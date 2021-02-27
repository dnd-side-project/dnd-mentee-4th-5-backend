from unittest import mock

import pytest

from shared_kernel.application.dtos import SuccessOutputDto
from shared_kernel.domain.value_objects import UserId, DrinkId
from wishes.application.dto import (
    CreateWishInputDto,
    CreateWishOutputDto,
    DeleteWishInputDto,
    FindWishesInputDto,
    FindWishesOutputDto,
)
from wishes.application.service import WishApplicationService
from wishes.domain.entities import Wish
from wishes.domain.repository import QueryParam, WishRepository
from wishes.domain.value_objects import WishId


@pytest.fixture(scope="function")
def wish_application_service():
    wish_repository_mock = mock.Mock(spec=WishRepository)
    wish_repository_mock.find_all.return_value = [
        Wish(
            id=WishId.build(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"),
            user_id=UserId(value="heumsi"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        ),
        Wish(
            id=WishId.build(user_id="joon", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"),
            user_id=UserId(value="joon"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        ),
    ]

    return WishApplicationService(wish_repository=wish_repository_mock)


@pytest.fixture(scope="function")
def drink_application_service():
    return mock.Mock()


def test_find_create_wish_success(wish_application_service):
    input_dto = FindWishesInputDto(query_param=QueryParam(drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    output_dto = wish_application_service.find_wishes(input_dto)
    assert output_dto.status is True
    assert output_dto.items == [
        FindWishesOutputDto.Item(
            id=str(WishId.build(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")),
            user_id="heumsi",
            drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
            created_at=1613113664.931505,
        ),
        FindWishesOutputDto.Item(
            id=str(WishId.build(user_id="joon", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")),
            user_id="joon",
            drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
            created_at=1613113664.931505,
        ),
    ]


def test_create_wish_success(
    wish_application_service,
    drink_application_service,
):
    drink_application_service.add_drink_wish.return_value = mock.Mock(spec=SuccessOutputDto)

    input_dto = CreateWishInputDto(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")
    output_dto = wish_application_service.create_wish(input_dto, drink_application_service)

    assert output_dto.status is True
    assert output_dto == CreateWishOutputDto(
        id=str(WishId.build(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")),
        user_id="heumsi",
        drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
        created_at=output_dto.created_at,
    )


def test_delete_wish_success(
    wish_application_service,
    drink_application_service,
):
    drink_application_service.delete_drink_wish.return_value = mock.Mock(spec=SuccessOutputDto)

    input_dto = DeleteWishInputDto(
        wish_id=str(WishId.build(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    )
    output_dto = wish_application_service.delete_wish(input_dto, drink_application_service)
    assert output_dto.status is True
