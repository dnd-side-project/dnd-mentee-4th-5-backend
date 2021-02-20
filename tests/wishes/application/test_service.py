import pytest

from drinks.application.dtos import CreateDrinkInputDto
from drinks.application.service import DrinkApplicationService
from drinks.domain.entities import Drink
from drinks.domain.value_objects import DrinkId as drinks_DrinkId
from drinks.domain.value_objects import DrinkRating, DrinkType
from drinks.infra_structure.in_memory_repository import InMemoryDrinkRepository
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
from wishes.domain.value_objects import DrinkId, UserId
from wishes.infra_structure.in_memory_repository import InMemoryWishRepository


@pytest.fixture
def wish_repository():
    return InMemoryWishRepository()


@pytest.fixture
def drink_repository():
    return InMemoryDrinkRepository()


@pytest.fixture(scope="function")
def wish_application_service(wish_repository, drink_repository):
    return WishApplicationService(wish_repository=wish_repository)


@pytest.fixture(scope="function")
def drink_application_service(drink_repository):
    return DrinkApplicationService(drink_repository=drink_repository)


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
            user_id="heumsi",
            drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
            created_at=1613113664.931505,
        ),
        FindWishesOutputDto.Item(
            user_id="joon",
            drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
            created_at=1613113664.931505,
        ),
        FindWishesOutputDto.Item(
            user_id="dongyoung",
            drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
            created_at=1613113664.931505,
        ),
    ]


def test_create_wish(
    wish_application_service,
    wish_repository,
    drink_application_service,
    drink_repository,
):
    input_dto = CreateDrinkInputDto(
        drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
        drink_name="Golden Ale",
        drink_image_url="picture of golden ale",
        drink_type=DrinkType.BEER,
    )
    drink_application_service.create_drink(input_dto)

    input_dto = CreateWishInputDto(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")
    output_dto = wish_application_service.create_wish(input_dto, drink_application_service)

    assert output_dto.status is True
    assert output_dto == CreateWishOutputDto(
        user_id="heumsi",
        drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
        created_at=output_dto.created_at,
    )
    # update num_of_wish field in drink entity
    actual = drink_repository.find_all_simple()
    expected = [
        Drink(
            id=drinks_DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            name="Golden Ale",
            image_url="picture of golden ale",
            type=DrinkType.BEER,
            avg_rating=DrinkRating(),
            num_of_reviews=0,
            num_of_wish=1,
        )
    ]
    assert actual == expected

    wish = wish_repository.find(QueryParam(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    assert wish is not None


def test_delete_wish(
    wish_application_service,
    wish_repository,
    drink_application_service,
    drink_repository,
):
    input_dto = CreateDrinkInputDto(
        drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c",
        drink_name="Golden Ale",
        drink_image_url="picture of golden ale",
        drink_type=DrinkType.BEER,
    )
    drink_application_service.create_drink(input_dto)

    wish_repository.add(
        Wish(
            user_id=UserId(value="heumsi"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613113664.931505,
        )
    )

    input_dto = DeleteWishInputDto(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c")
    output_dto = wish_application_service.delete_wish(input_dto, drink_application_service)
    assert output_dto.status is True
