import pytest

from wishes.application.dto import (
    CreateWishInputDto,
    CreateWishOutputDto,
    DeleteWishInputDto,
    FindWishesInputDto,
    FindWishesOutputDto,
)
from wishes.application.service import WishApplicationService
from wishes.domain.entities import Wish
from wishes.domain.repository import QueryParam
from wishes.domain.value_objects import UserId, DrinkId
from wishes.infra_structure.in_memory_repository import InMemoryWishRepository


@pytest.fixture
def wish_repository():
    return InMemoryWishRepository()


@pytest.fixture(scope="function")
def wish_application_service(wish_repository):
    return WishApplicationService(wish_repository=wish_repository)


def test_find_create_wish(wish_application_service, wish_repository):
    wish_repository.add(
        Wish(
            user_id=UserId(value="heumsi"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        )
    )
    wish_repository.add(
        Wish(
            user_id=UserId(value="joon"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        )
    )
    wish_repository.add(
        Wish(
            user_id=UserId(value="dongyoung"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        )
    )

    input_dto = FindWishesInputDto(
        query_param=QueryParam(user_id=None, drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")
    )
    output_dto = wish_application_service.find_wishes(input_dto)
    assert output_dto.status is True
    assert output_dto.items == [
        FindWishesOutputDto.Item(
            user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c", created_at=1613113664.931505
        ),
        FindWishesOutputDto.Item(
            user_id="joon", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c", created_at=1613113664.931505
        ),
        FindWishesOutputDto.Item(
            user_id="dongyoung", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c", created_at=1613113664.931505
        ),
    ]


def test_create_wish(wish_application_service, wish_repository):
    input_dto = CreateWishInputDto(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")
    output_dto = wish_application_service.create_wish(input_dto)
    assert output_dto.status is True
    assert output_dto == CreateWishOutputDto(
        user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c", created_at=output_dto.created_at
    )
    wish = wish_repository.find(QueryParam(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    assert wish is not None


def test_delete_wish(wish_application_service, wish_repository):
    wish_repository.add(
        Wish(
            user_id=UserId(value="heumsi"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        )
    )

    input_dto = DeleteWishInputDto(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")
    output_dto = wish_application_service.delete_wish(input_dto)
    assert output_dto.status is True
