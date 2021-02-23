from unittest import mock

import pytest
from drinks.application.dtos import (AddDrinkReviewOutputDto,
                                     DeleteDrinkReviewOutputDto,
                                     UpdateDrinkReviewOutputDto)
from drinks.application.service import DrinkApplicationService
from reviews.application.dtos import (CreateReviewInputDto,
                                      CreateReviewOutputDto,
                                      DeleteReviewInputDto,
                                      DeleteReviewOutputDto,
                                      FindReviewInputDto, FindReviewOutputDto,
                                      FindReviewsInputDto,
                                      FindReviewsOutputDto,
                                      UpdateReviewInputDto,
                                      UpdateReviewOutputDto)
from reviews.application.service import ReviewApplicationService
from reviews.domain.entities import Review
from reviews.domain.repository import QueryParam, ReviewRepository
from reviews.domain.value_objects import ReviewRating
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import (InvalidParamInputError,
                                             ResourceAlreadyExistError,
                                             ResourceNotFoundError)
from shared_kernel.domain.value_objects import DrinkId, ReviewId, UserId

review_data = [
    (
        ReviewId.build(
            user_id="Jun", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"
        ),  # review_id
        DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),  # drink_id
        "Jun",  # user_id
        4,  # rating
        1355563265.81,  # created_at
    )
]


@pytest.fixture(scope="function")
def review_repository_mock():
    return mock.Mock(spec=ReviewRepository)


@pytest.fixture(scope="function")
def drink_application_service_mock():
    return mock.Mock(spec=DrinkApplicationService)


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_find_review_success(
    review_repository_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_by_review_id.return_value = Review(
        id=review_id,
        drink_id=drink_id,
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="hello",
        created_at=created_at,
        updated_at=created_at,
    )
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    input_dto = FindReviewInputDto(review_id=str(review_id))

    actual = review_application_service.find_review(input_dto)
    expected = FindReviewOutputDto(
        review_id=str(review_id),
        drink_id=str(drink_id),
        user_id=str(UserId(value=user_id)),
        rating=int(ReviewRating(value=rating)),
        comment="hello",
        created_at=created_at,
        updated_at=created_at,
    )
    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_find_review_fail(
    review_repository_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_by_review_id.side_effect = ResourceNotFoundError()
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    input_dto = FindReviewInputDto(review_id=str(review_id))
    actual = review_application_service.find_review(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")

    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_find_reviews_success(
    review_repository_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    drink_id_2 = "335ca1a4-5175-5e41-8bac-40ffd840835c"
    user_id_2 = "meme"
    review_id_2 = ReviewId.build(user_id=user_id_2, drink_id=drink_id_2)

    review_repository_mock.find_all.return_value = [
        Review(
            id=review_id,
            drink_id=drink_id,
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="hello",
            created_at=created_at,
            updated_at=created_at,
        ),
        Review(
            id=review_id_2,
            drink_id=DrinkId.from_str(drink_id_2),
            user_id=UserId(value=user_id_2),
            rating=ReviewRating(value=rating),
            comment="olleh",
            created_at=created_at,
            updated_at=created_at,
        ),
    ]
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    input_dto = FindReviewsInputDto(query_param=QueryParam())
    actual = review_application_service.find_reviews(input_dto)
    expected = FindReviewsOutputDto(
        items=[
            FindReviewsOutputDto.Item(
                review_id=str(review_id),
                drink_id=str(drink_id),
                user_id=str(user_id),
                rating=int(rating),
                comment="hello",
                created_at=created_at,
                updated_at=created_at,
            ),
            FindReviewsOutputDto.Item(
                review_id=str(review_id_2),
                drink_id=str(drink_id_2),
                user_id=str(user_id_2),
                rating=int(rating),
                comment="olleh",
                created_at=created_at,
                updated_at=created_at,
            ),
        ]
    )
    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_find_reviews_fail(
    review_repository_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_all.side_effect = InvalidParamInputError()
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    input_dto = FindReviewsInputDto(query_param=QueryParam())
    actual = review_application_service.find_reviews(input_dto)
    expected = FailedOutputDto(type="Parameters Error", message="")

    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_create_review_success(
    app,
    review_repository_mock,
    drink_application_service_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.add.return_value = None
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    drink_application_service_mock.add_drink_review.return_value = (
        AddDrinkReviewOutputDto()
    )
    with app.container.drink_application_service.override(
        drink_application_service_mock
    ):
        input_dto = CreateReviewInputDto(
            drink_id=str(drink_id),
            user_id=user_id,
            rating=int(ReviewRating(value=rating)),
            comment="",
        )

        actual = review_application_service.create_review(
            input_dto, drink_application_service_mock
        )
        expected = CreateReviewOutputDto(
            review_id=str(review_id),
            drink_id=str(drink_id),
            user_id=user_id,
            rating=rating,
            comment="",
            created_at=actual.created_at,
            updated_at=actual.updated_at,
        )

        assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_create_review_fail(
    review_repository_mock,
    drink_application_service_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.add.side_effect = ResourceAlreadyExistError()
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    drink_application_service_mock.add_drink_review.return_value = (
        AddDrinkReviewOutputDto()
    )

    input_dto = CreateReviewInputDto(
        drink_id=str(drink_id),
        user_id=str(UserId(value=user_id)),
        rating=int(ReviewRating(value=rating)),
        comment="",
    )

    actual = review_application_service.create_review(
        input_dto, drink_application_service_mock
    )
    expected = FailedOutputDto(type="Resource Conflict Error", message="")
    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_update_review_success(
    review_repository_mock,
    drink_application_service_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_by_review_id.return_value = Review(
        id=review_id,
        drink_id=drink_id,
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="hello",
        created_at=created_at,
        updated_at=created_at,
    )
    review_repository_mock.update.return_value = None
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    drink_application_service_mock.update_drink_review.return_value = (
        UpdateDrinkReviewOutputDto()
    )

    input_dto = UpdateReviewInputDto(
        review_id=str(review_id),
        rating=int(ReviewRating(value=rating)),
        comment="",
    )

    actual = review_application_service.update_review(
        input_dto, drink_application_service_mock
    )
    expected = UpdateReviewOutputDto()
    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_update_review_fail(
    review_repository_mock,
    drink_application_service_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_by_review_id.return_value = Review(
        id=review_id,
        drink_id=drink_id,
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="hello",
        created_at=created_at,
        updated_at=created_at,
    )
    review_repository_mock.update.side_effect = ResourceNotFoundError()
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    drink_application_service_mock.update_drink_review.return_value = (
        UpdateDrinkReviewOutputDto()
    )

    input_dto = UpdateReviewInputDto(
        review_id=str(review_id),
        rating=int(ReviewRating(value=rating)),
        comment="",
    )
    actual = review_application_service.update_review(
        input_dto, drink_application_service_mock
    )
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_delete_review_success(
    review_repository_mock,
    drink_application_service_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_by_review_id.return_value = Review(
        id=review_id,
        drink_id=drink_id,
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="hello",
        created_at=created_at,
        updated_at=created_at,
    )
    review_repository_mock.delete_by_review_id.return_value = None
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    drink_application_service_mock.delete_drink_review.return_value = (
        DeleteDrinkReviewOutputDto()
    )

    input_dto = DeleteReviewInputDto(review_id=str(review_id))

    actual = review_application_service.delete_review(
        input_dto, drink_application_service_mock
    )
    expected = DeleteReviewOutputDto()
    assert actual == expected


@pytest.mark.parametrize(
    "review_id, drink_id, user_id, rating, created_at", review_data
)
def test_delete_review_fail(
    review_repository_mock,
    drink_application_service_mock,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository_mock.find_by_review_id.return_value = Review(
        id=review_id,
        drink_id=drink_id,
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="hello",
        created_at=created_at,
        updated_at=created_at,
    )
    review_repository_mock.delete_by_review_id.side_effect = ResourceNotFoundError()
    review_application_service = ReviewApplicationService(
        review_repository=review_repository_mock
    )

    drink_application_service_mock.delete_drink_review.return_value = (
        DeleteDrinkReviewOutputDto()
    )

    input_dto = DeleteReviewInputDto(review_id=str(review_id))
    actual = review_application_service.delete_review(
        input_dto, drink_application_service_mock
    )
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected
