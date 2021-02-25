import pytest

from drinks.domain.entities import Drink
from drinks.domain.value_objects import DrinkType, DrinkRating
from shared_kernel.domain.value_objects import DrinkId


@pytest.fixture(scope="function")
def drink_no_review():
    return Drink(
        id=DrinkId.build(drink_name="soju1", created_at=1234),
        name="soju1",
        image_url="soju_image1",
        type=DrinkType.from_str("soju"),
        avg_rating=DrinkRating(),
        num_of_reviews=0,
        num_of_wish=0,
    )


@pytest.fixture(scope="function")
def drink_one_review():
    return Drink(
        id=DrinkId.build(drink_name="soju2", created_at=1234),
        name="soju2",
        image_url="soju_image2",
        type=DrinkType.from_str("soju"),
        avg_rating=DrinkRating(value=5),
        num_of_reviews=1,
        num_of_wish=1,
    )


@pytest.fixture(scope="function")
def drink_two_reviews():
    return Drink(
        id=DrinkId.build(drink_name="soju3", created_at=1234),
        name="soju3",
        image_url="soju_image3",
        type=DrinkType.from_str("soju"),
        avg_rating=DrinkRating(value=4.5),
        num_of_reviews=2,
        num_of_wish=2,
    )


def test_drink_add_rating(drink_no_review, drink_one_review, drink_two_reviews):
    drink_no_review.add_rating(input_rating=5)
    assert drink_no_review.avg_rating == DrinkRating(value=5)
    assert drink_no_review.num_of_reviews == 1


def test_drink_update_rating(drink_no_review, drink_one_review, drink_two_reviews):
    drink_no_review.update_rating(old_rating=5, new_rating=4)
    assert drink_no_review.avg_rating == DrinkRating(value=0)
    assert drink_no_review.num_of_reviews == 0

    drink_one_review.update_rating(old_rating=5, new_rating=4)
    assert drink_one_review.avg_rating == DrinkRating(value=4)
    assert drink_one_review.num_of_reviews == 1

    drink_two_reviews.update_rating(old_rating=4, new_rating=5)
    assert drink_two_reviews.avg_rating == DrinkRating(value=5)
    assert drink_two_reviews.num_of_reviews == 2


def test_drink_delete_rating(drink_no_review, drink_one_review, drink_two_reviews):
    drink_no_review.delete_rating(input_rating=5)
    assert drink_no_review.avg_rating == DrinkRating(value=0)
    assert drink_no_review.num_of_reviews == 0

    drink_one_review.delete_rating(input_rating=5)
    assert drink_one_review.avg_rating == DrinkRating(value=0)
    assert drink_one_review.num_of_reviews == 0

    drink_two_reviews.delete_rating(input_rating=5)
    assert drink_two_reviews.avg_rating == DrinkRating(value=4)
    assert drink_two_reviews.num_of_reviews == 1


def test_drink_add_wish(drink_no_review, drink_one_review, drink_two_reviews):
    drink_no_review.add_wish()
    assert drink_no_review.num_of_wish == 1

    drink_no_review.add_wish()
    assert drink_no_review.num_of_wish == 2


def test_drink_delete_wish(drink_no_review, drink_one_review, drink_two_reviews):
    drink_no_review.delete_wish()
    assert drink_no_review.num_of_wish == 0

    drink_one_review.delete_wish()
    assert drink_one_review.num_of_wish == 0

    drink_two_reviews.delete_wish()
    assert drink_two_reviews.num_of_wish == 1
