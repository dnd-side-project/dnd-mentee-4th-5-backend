import pytest
from reviews.application.dtos import (
    CreateReviewInputDto,
    DeleteReviewInputDto,
    FindReviewInputDto,
    FindReviewOutputDto,
    UpdateReviewInputDto,
)
from reviews.application.service import ReviewApplicationService
from reviews.domain.entities import Review
from reviews.domain.value_objects import ReviewRating, UserId, ReviewId, DrinkId
from reviews.infra_structure.in_memory_repository import InMemoryReviewRepository
from shared_kernel.application.dtos import FailedOutputDto


@pytest.fixture
def review_repository():
    return InMemoryReviewRepository()


@pytest.fixture
def review_application_service(review_repository):
    return ReviewApplicationService(review_repository=review_repository)


review_data = [
    (
        ReviewId.build(user_id="Jun", drink_id="335ca1a4-5175-5e41-8bac-40ffd840834c"),  # review_id
        DrinkId.from_str("335ca1a4-5175-5e41-8bac-40ffd840834c"),  # drink_id
        "Jun",  # user_id
        4,  # rating
        1355563265.81,  # created_at
    )
]


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
            id=review_id,
            drink_id=drink_id,
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="hello",
            created_at=created_at,
            updated_at=created_at,
        )
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
        drink_id=str(drink_id),
        user_id=str(UserId(value=user_id)),
        rating=int(ReviewRating(value=rating)),
        comment="",
    )

    output_dto = review_application_service.create_review(input_dto)
    assert output_dto.status

    actual = review_repository.find_all()
    expected = [
        Review(
            id=review_id,
            drink_id=drink_id,
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=output_dto.created_at,
            updated_at=output_dto.updated_at,
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
            id=review_id,
            drink_id=drink_id,
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=created_at,
            updated_at=created_at,
        )
    )

    input_dto = UpdateReviewInputDto(
        review_id=str(review_id),
        rating=int(ReviewRating(value=rating)),
        comment="This drink sucks",
    )
    review_application_service.update_review(input_dto)

    actual = review_repository.find_by_review_id(review_id=review_id)
    assert actual.comment == "This drink sucks"
    assert actual.updated_at != created_at


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
            id=review_id,
            drink_id=drink_id,
            user_id=UserId(value=user_id),
            rating=ReviewRating(value=rating),
            comment="",
            created_at=created_at,
            updated_at=created_at,
        )
    )

    input_dto = DeleteReviewInputDto(review_id=str(review_id))
    review_application_service.delete_review(input_dto)

    actual = review_repository.find_by_review_id(review_id=review_id)
    expected = None
    assert actual == expected

    # Check delete when review in-memory repo is empty
    actual = review_application_service.delete_review(input_dto)
    expected = FailedOutputDto.build_resource_not_found_error(f"{str(review_id)}의 리뷰를 찾을 수 없습니다.")
    assert actual == expected


"""
아래 코드는 현재 미사용
"""
#
# @pytest.mark.parametrize("review_id, drink_id, user_id, rating, created_at", review_data)
# def test_find_reviews_by_user_id(
#     review_application_service,
#     review_repository,
#     review_id,
#     drink_id,
#     user_id,
#     rating,
#     created_at,
# ):
#     review_repository.add(
#         Review(
#             id=review_id,
#             drink_id=drink_id,
#             user_id=UserId(value=user_id),
#             rating=ReviewRating(value=rating),
#             comment="",
#             created_at=created_at,
#         )
#     )
#     review_repository.add(
#         Review(
#             id=uuid.uuid4(),
#             drink_id=drink_id,
#             user_id=UserId(value="diff_user_id"),
#             rating=ReviewRating(value=rating),
#             comment="Won't match the user_id",
#             created_at=1234,
#         )
#     )
#
#     input_dto = FindReviewsByUserIdInputDto(user_id=str(UserId(value=user_id)))
#     actual = review_application_service.find_reviews_by_user_id(input_dto=input_dto)
#     expected = FindReviewsByUserIdOutputDto(
#         reviews_dicts=[
#             Review(
#                 id=review_id,
#                 drink_id=drink_id,
#                 user_id=UserId(value=user_id),
#                 rating=ReviewRating(value=rating),
#                 comment="",
#                 created_at=created_at,
#             ).dict()
#         ]
#     )
#     assert actual == expected
#
#
# @pytest.mark.parametrize("review_id, drink_id, user_id, rating, created_at", review_data)
# def test_find_reviews_by_drink_id(
#     review_application_service,
#     review_repository,
#     review_id,
#     drink_id,
#     user_id,
#     rating,
#     created_at,
# ):
#     review_repository.add(
#         Review(
#             id=review_id,
#             drink_id=drink_id,
#             user_id=UserId(value=user_id),
#             rating=ReviewRating(value=rating),
#             comment="",
#             created_at=created_at,
#         )
#     )
#     review_repository.add(
#         Review(
#             id=uuid.uuid4(),
#             drink_id=uuid.uuid4(),
#             user_id=UserId(value=user_id),
#             rating=ReviewRating(value=rating),
#             comment="Won't match the drink_id",
#             created_at=1234,
#         )
#     )
#
#     input_dto = FindReviewsByDrinkIdInputDto(drink_id=str(drink_id))
#     actual = review_application_service.find_reviews_by_drink_id(input_dto=input_dto)
#     expected = FindReviewsByDrinkIdOutputDto(
#         reviews_dicts=[
#             Review(
#                 id=review_id,
#                 drink_id=drink_id,
#                 user_id=UserId(value=user_id),
#                 rating=ReviewRating(value=rating),
#                 comment="",
#                 created_at=created_at,
#             ).dict()
#         ]
#     )
#     assert actual == expected
