import pytest

from drinks.domain.entities import Drink
from drinks.domain.repository import QueryParam
from drinks.domain.value_objects import DrinkType, DrinkRating, OrderType, FilterType
from drinks.infra_structure.orm_models import DrinkOrm
from drinks.infra_structure.orm_repository import OrmDrinkRepository
from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from shared_kernel.domain.value_objects import DrinkId


@pytest.fixture(scope="session", autouse=True)
def setup(database):
    with database.session() as session:
        session.query(DrinkOrm).delete()
        session.add_all(
            [
                DrinkOrm.from_drink(
                    Drink(
                        id=DrinkId.build(drink_name="soju1", created_at=1234),
                        name="soju1",
                        image_url="soju_image1",
                        type=DrinkType.SOJU,
                        avg_rating=DrinkRating(),
                        num_of_reviews=0,
                        num_of_wish=0,
                    )
                ),
                DrinkOrm.from_drink(
                    Drink(
                        id=DrinkId.build(drink_name="soju2", created_at=1234),
                        name="soju2",
                        image_url="soju_image2",
                        type=DrinkType.SOJU,
                        avg_rating=DrinkRating(value=5),
                        num_of_reviews=1,
                        num_of_wish=1,
                    )
                ),
                DrinkOrm.from_drink(
                    Drink(
                        id=DrinkId.build(drink_name="beer", created_at=1234),
                        name="beer",
                        image_url="beer_image",
                        type=DrinkType.BEER,
                        avg_rating=DrinkRating(value=4.5),
                        num_of_reviews=2,
                        num_of_wish=2,
                    )
                ),
            ]
        )
        session.commit()


@pytest.fixture(scope="function")
def orm_drink_repository(database):
    return OrmDrinkRepository(session_factory=database.session)


def test_find_by_review_id(orm_drink_repository):
    with pytest.raises(ResourceNotFoundError):
        orm_drink_repository.find_by_drink_id(DrinkId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbd8"))

    a = DrinkOrm.from_drink(
        Drink(
            id=DrinkId.build(drink_name="soju1", created_at=1234),
            name="soju1",
            image_url="soju_image1",
            type=DrinkType.SOJU,
            avg_rating=DrinkRating(),
            num_of_reviews=0,
            num_of_wish=0,
        )
    )

    actual = orm_drink_repository.find_by_drink_id(drink_id=DrinkId.build(drink_name="soju1", created_at=1234))
    expected = Drink(
        id=DrinkId.build(drink_name="soju1", created_at=1234),
        name="soju1",
        image_url="soju_image1",
        type=DrinkType.from_str("soju"),
        avg_rating=DrinkRating(),
        num_of_reviews=0,
        num_of_wish=0,
    )
    assert actual == expected


def test_find_all(orm_drink_repository):
    actual = orm_drink_repository.find_all(
        query_param=QueryParam(
            type=DrinkType.from_str("soju"),
            filter=FilterType.from_str("review"),
            order=OrderType.from_str("descending"),
        )
    )
    expected = [
        Drink(
            id=DrinkId.build(drink_name="soju2", created_at=1234),
            name="soju2",
            image_url="soju_image2",
            type=DrinkType.from_str("soju"),
            avg_rating=DrinkRating(value=5),
            num_of_reviews=1,
            num_of_wish=1,
        ),
        Drink(
            id=DrinkId.build(drink_name="soju1", created_at=1234),
            name="soju1",
            image_url="soju_image1",
            type=DrinkType.from_str("soju"),
            avg_rating=DrinkRating(),
            num_of_reviews=0,
            num_of_wish=0,
        ),
    ]
    assert actual == expected


def test_add(orm_drink_repository):
    drink = Drink(
        id=DrinkId.build(drink_name="wine", created_at=1234),
        name="wine",
        image_url="wine_image",
        type=DrinkType.from_str("wine"),
        avg_rating=DrinkRating(value=3),
        num_of_reviews=1,
        num_of_wish=1,
    )
    orm_drink_repository.add(drink)

    actual = orm_drink_repository.find_by_drink_id(drink_id=DrinkId.build(drink_name="wine", created_at=1234))
    expected = Drink(
        id=DrinkId.build(drink_name="wine", created_at=1234),
        name="wine",
        image_url="wine_image",
        type=DrinkType.from_str("wine"),
        avg_rating=DrinkRating(value=3),
        num_of_reviews=1,
        num_of_wish=1,
    )

    assert actual == expected

    with pytest.raises(ResourceAlreadyExistError):
        orm_drink_repository.add(drink)


def test_update(orm_drink_repository):
    old_drink = orm_drink_repository.find_by_drink_id(DrinkId.build(drink_name="soju1", created_at=1234))

    new_drink = Drink(
        id=old_drink.id,
        name=old_drink.name,
        image_url=old_drink.image_url,
        type=old_drink.type,
        avg_rating=DrinkRating(value=4.5),
        num_of_reviews=2,
        num_of_wish=1,
    )
    orm_drink_repository.update(new_drink)

    actual = orm_drink_repository.find_by_drink_id(DrinkId.build(drink_name="soju1", created_at=1234))
    expected = new_drink
    assert actual == expected


def test_delete(orm_drink_repository):
    orm_drink_repository.find_by_drink_id(drink_id=DrinkId.build(drink_name="soju1", created_at=1234))

    orm_drink_repository.delete_by_drink_id(drink_id=DrinkId.build(drink_name="soju1", created_at=1234))

    with pytest.raises(ResourceNotFoundError):
        orm_drink_repository.delete_by_drink_id(drink_id=DrinkId.build(drink_name="soju1", created_at=1234))
