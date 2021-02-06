import datetime
import uuid

import pytest
from reviews.application.dtos import (
    CreateReviewInputDto,
    DeleteReviewInputDto,
    FindReviewInputDto,
    FindReviewOutputDto,
    UpdateReviewInputDto,
)
from reviews.application.exceptions import ReviewNotExistError
from reviews.application.service import ReviewApplicationService
from reviews.domain.entities import Review
from reviews.domain.value_objects import ReviewRating
from reviews.infra_structure.in_memory_repository import InMemoryReviewRepository
from users.domain.value_objects import UserId


@pytest.fixture
def review_repository():
    return InMemoryReviewRepository()


@pytest.fixture
def review_application_service(review_repository):
    return ReviewApplicationService(review_repository=review_repository)


review_data = [("review_id", "drink_id", "Jun", 4, 1355563265.81)]


@pytest.mark.parametrize("review_id, drink_id, user_id, rating, created_at", review_data)
def test_find_review(
    review_application_service,
    review_repository,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository.add(
        Review(
            id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
            drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=created_at,
        )
    )
    input_dto = FindReviewInputDto(review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id))

    actual = review_application_service.find_review(input_dto)
    expected = FindReviewOutputDto(
        review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
        drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="",
        created_at=created_at,
    )
    assert actual == expected


@pytest.mark.parametrize("review_id, drink_id, user_id, rating, created_at", review_data)
def test_create_review(
    review_application_service,
    review_repository,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    input_dto = CreateReviewInputDto(
        review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
        drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="",
        created_at=created_at,
    )

    review_application_service.create_review(input_dto)
    actual = review_repository.find_all()
    expected = [
        Review(
            id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
            drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=created_at,
        )
    ]
    assert actual == expected


@pytest.mark.parametrize("review_id, drink_id, user_id, rating, created_at", review_data)
def test_update_review(
    review_application_service,
    review_repository,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository.add(
        Review(
            id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
            drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=created_at,
        )
    )

    input_dto = UpdateReviewInputDto(
        review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
        drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="This drink sucks",
        created_at=created_at,
    )
    review_application_service.update_review(input_dto)

    actual = review_repository.find_by_review_id(review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id))
    expected = Review(
        id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
        drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
        user_id=UserId(value=user_id),
        rating=ReviewRating(value=rating),
        comment="This drink sucks",
        created_at=created_at,
    )
    assert actual == expected


@pytest.mark.parametrize("review_id, drink_id, user_id, rating, created_at", review_data)
def test_delete_review(
    review_application_service,
    review_repository,
    review_id,
    drink_id,
    user_id,
    rating,
    created_at,
):
    review_repository.add(
        Review(
            id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id),
            drink_id=uuid.uuid5(uuid.NAMESPACE_DNS, drink_id),
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=created_at,
        )
    )

    input_dto = DeleteReviewInputDto(review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id))
    review_application_service.delete_review(input_dto)

    actual = review_repository.find_by_review_id(review_id=uuid.uuid5(uuid.NAMESPACE_DNS, review_id))
    expected = None
    assert actual == expected

    # Check delete when review in-memory repo is empty
    with pytest.raises(ReviewNotExistError):
        review_application_service.delete_review(input_dto)
