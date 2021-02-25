import uuid

import pytest
from reviews.domain.entities import Review
from reviews.domain.repository import QueryParam
from reviews.domain.value_objects import ReviewRating
from reviews.infra_structure.orm_models import ReviewOrm
from reviews.infra_structure.orm_repository import OrmReviewRepository
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import ResourceAlreadyExistError, ResourceNotFoundError, InvalidParamInputError
from shared_kernel.domain.value_objects import DrinkId, ReviewId, UserId


@pytest.fixture(scope="session", autouse=True)
def setup(database):
    with database.session() as session:
        session.query(ReviewOrm).delete()
        session.add_all(
            [
                ReviewOrm.from_review(
                    Review(
                        id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"),
                        user_id=UserId(value="jun"),
                        drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
                        rating=ReviewRating(value=4),
                        comment="first jun",
                        created_at=1613807667,
                        updated_at=3,
                    )
                ),
                ReviewOrm.from_review(
                    Review(
                        id=ReviewId.from_str("b329c178-46e3-4d67-9ae4-6624b651d3d1"),
                        user_id=UserId(value="heumsi"),
                        drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
                        rating=ReviewRating(value=3),
                        comment="first heumsi",
                        created_at=1613807667,
                        updated_at=1,
                    )
                ),
                ReviewOrm.from_review(
                    Review(
                        id=ReviewId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
                        user_id=UserId(value="jun"),
                        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834d"),
                        rating=ReviewRating(value=4),
                        comment="second jun",
                        created_at=1613807667,
                        updated_at=2,
                    )
                ),
            ]
        )
        session.commit()


@pytest.fixture(scope="function")
def orm_review_repository(database):
    return OrmReviewRepository(session_factory=database.session)


def test_find(orm_review_repository):
    actual = orm_review_repository.find(
        query_param=QueryParam(drink_id="07a9627a-c930-4292-afd0-b6a2d55de3b2", user_id="jun")
    )
    expected = Review(
        id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"),
        user_id=UserId(value="jun"),
        drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
        rating=ReviewRating(value=4),
        comment="first jun",
        created_at=1613807667,
        updated_at=3,
    )
    assert actual == expected

    with pytest.raises(InvalidParamInputError):
        orm_review_repository.find(query_param=QueryParam(user_id="jun"))

    with pytest.raises(InvalidParamInputError):
        orm_review_repository.find(query_param=QueryParam(drink_id="07a9627a-c930-4292-afd0-b6a2d55de3b2"))


def test_find_all(orm_review_repository):
    actual = orm_review_repository.find_all(QueryParam(drink_id="07a9627a-c930-4292-afd0-b6a2d55de3b2"))
    expected = [
        Review(
            id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"),
            user_id=UserId(value="jun"),
            drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
            rating=ReviewRating(value=4),
            comment="first jun",
            created_at=1613807667,
            updated_at=3,
        ),
        Review(
            id=ReviewId.from_str("b329c178-46e3-4d67-9ae4-6624b651d3d1"),
            user_id=UserId(value="heumsi"),
            drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
            rating=ReviewRating(value=3),
            comment="first heumsi",
            created_at=1613807667,
            updated_at=1,
        ),
    ]
    assert actual == expected

    actual = orm_review_repository.find_all(QueryParam(user_id="jun"))
    expected = [
        Review(
            id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"),
            user_id=UserId(value="jun"),
            drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
            rating=ReviewRating(value=4),
            comment="first jun",
            created_at=1613807667,
            updated_at=3,
        ),
        Review(
            id=ReviewId.from_str("bcbfdb54-acb7-5443-926a-42e882ef7db0"),
            user_id=UserId(value="jun"),
            drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834d"),
            rating=ReviewRating(value=4),
            comment="second jun",
            created_at=1613807667,
            updated_at=2,
        ),
    ]
    assert actual == expected


def test_find_by_review_id(orm_review_repository):
    with pytest.raises(ResourceNotFoundError):
        orm_review_repository.find_by_review_id(ReviewId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbd8"))

    actual = orm_review_repository.find_by_review_id(
        review_id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367")
    )
    expected = Review(
        id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"),
        user_id=UserId(value="jun"),
        drink_id=DrinkId.from_str("07a9627a-c930-4292-afd0-b6a2d55de3b2"),
        rating=ReviewRating(value=4),
        comment="first jun",
        created_at=1613807667,
        updated_at=3,
    )
    assert actual == expected


# def test_find_all(orm_wish_repository):


def test_add(orm_review_repository):
    review = Review(
        id=ReviewId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbc1"),
        user_id=UserId(value="ME"),
        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
        rating=ReviewRating(value=4),
        comment="456",
        created_at=1613807667,
        updated_at=1613807667,
    )
    orm_review_repository.add(review)

    actual = orm_review_repository.find_by_review_id(
        review_id=ReviewId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbc1")
    )
    expected = Review(
        id=ReviewId.from_str("35a05a4b-d9ba-5122-af75-7c0022b8bbc1"),
        user_id=UserId(value="ME"),
        drink_id=DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),
        rating=ReviewRating(value=4),
        comment="456",
        created_at=1613807667,
        updated_at=1613807667,
    )
    assert actual == expected

    with pytest.raises(ResourceAlreadyExistError):
        orm_review_repository.add(review)


def test_delete(orm_review_repository):
    orm_review_repository.find_by_review_id(review_id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"))

    orm_review_repository.delete_by_review_id(review_id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"))

    with pytest.raises(ResourceNotFoundError):
        orm_review_repository.delete_by_review_id(review_id=ReviewId.from_str("afa213dd-d705-4f4d-953d-ad25e7181367"))
