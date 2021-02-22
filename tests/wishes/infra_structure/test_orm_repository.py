import uuid

import pytest

from shared_kernel.domain.exceptions import ResourceAlreadyExistError, ResourceNotFoundError
from shared_kernel.domain.value_objects import UserId, DrinkId
from wishes.domain.entities import Wish
from wishes.domain.repository import QueryParam
from wishes.domain.value_objects import WishId
from wishes.infra_structure.orm_models import WishOrm
from wishes.infra_structure.orm_repository import OrmWishRepository


@pytest.fixture(scope="session", autouse=True)
def setup(database):
    with database.session() as session:
        session.query(WishOrm).delete()
        session.add_all(
            [
                WishOrm.from_wish(
                    Wish(
                        id=WishId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
                        user_id=UserId(value="heumsi"),
                        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
                        created_at=1613807667,
                    )
                ),
                WishOrm.from_wish(
                    Wish(
                        id=WishId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbd9"),
                        user_id=UserId(value="joon"),
                        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
                        created_at=1613807667,
                    )
                ),
            ]
        )
        session.commit()


@pytest.fixture(scope="function")
def orm_wish_repository(database):
    return OrmWishRepository(session_factory=database.session)


def test_find(orm_wish_repository):
    actual = orm_wish_repository.find(QueryParam(user_id="heumsi"))
    expected = Wish(
        id=WishId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
        user_id=UserId(value="heumsi"),
        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
        created_at=1613807667.0,
    )
    assert actual == expected

    actual = orm_wish_repository.find(QueryParam(user_id="heumsi", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    expected = Wish(
        id=WishId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
        user_id=UserId(value="heumsi"),
        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
        created_at=1613807667.0,
    )
    assert actual == expected


def test_find_all(orm_wish_repository):
    actual = orm_wish_repository.find_all(QueryParam(drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    expected = [
        Wish(
            id=WishId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
            user_id=UserId(value="heumsi"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613807667.0,
        ),
        Wish(
            id=WishId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbd9"),
            user_id=UserId(value="joon"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
            created_at=1613807667.0,
        ),
    ]
    assert actual == expected


def test_add(orm_wish_repository):
    wish = Wish(
        id=WishId.build(user_id="siheum", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"),
        user_id=UserId(value="siheum"),
        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
        created_at=1613807667,
    )
    orm_wish_repository.add(wish)

    actual = orm_wish_repository.find(QueryParam(user_id="siheum", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"))
    expected = wish
    assert actual == expected

    with pytest.raises(ResourceAlreadyExistError):
        orm_wish_repository.add(wish)


def test_delete(orm_wish_repository):
    with pytest.raises(ResourceNotFoundError):
        orm_wish_repository.find(QueryParam(user_id="not exist user"))

    actual = orm_wish_repository.delete_by_wish_id(wish_id=WishId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"))
    expected = Wish(
        id=WishId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
        user_id=UserId(value="heumsi"),
        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
        created_at=1613807667.0,
    )
    assert actual == expected

    with pytest.raises(ResourceNotFoundError):
        orm_wish_repository.find(query_param=QueryParam(user_id="heumsi"))
