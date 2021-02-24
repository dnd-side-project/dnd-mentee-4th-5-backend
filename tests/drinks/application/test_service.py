from unittest import mock

import pytest

from drinks.application.dtos import (
    AddDrinkReviewInputDto,
    CreateDrinkInputDto,
    DeleteDrinkInputDto,
    DeleteDrinkReviewInputDto,
    FindDrinkInputDto,
    FindDrinkOutputDto,
    UpdateDrinkInputDto,
    CreateDrinkOutputDto,
    UpdateDrinkOutputDto,
    DeleteDrinkOutputDto,
    AddDrinkReviewOutputDto,
    UpdateDrinkReviewOutputDto,
    UpdateDrinkReviewInputDto,
    DeleteDrinkReviewOutputDto,
    AddDrinkWishInputDto,
    AddDrinkWishOutputDto,
    DeleteDrinkWishOutputDto,
    DeleteDrinkWishInputDto,
)
from drinks.application.service import DrinkApplicationService
from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository
from drinks.domain.value_objects import DrinkRating, DrinkType
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from shared_kernel.domain.value_objects import DrinkId


@pytest.fixture(scope="function")
def drink_repository_mock():
    return mock.Mock(spec=DrinkRepository)


drink_data = [
    (
        DrinkId.build(drink_name="Cabernet", created_at=1234),
        "Cabernet",
        "wine_image_url",
        DrinkType.WINE,
    )
]


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_find_drink_success(
    client,
    app,
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)
    input_dto = FindDrinkInputDto(drink_id=str(drink_id))
    actual = drink_application_service.find_drink(input_dto)
    expected = FindDrinkOutputDto(
        drink_id=str(drink_id),
        drink_name=drink_name,
        drink_image_url=drink_image_url,
        drink_type=drink_type.value,
        avg_rating=float(DrinkRating()),
        num_of_reviews=0,
        num_of_wish=0,
    )
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_find_drink_fail(
    client,
    app,
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.side_effect = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)
    input_dto = FindDrinkInputDto(drink_id=str(drink_id))
    actual = drink_application_service.find_drink(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_create_drink_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.add.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)
    input_dto = CreateDrinkInputDto(
        drink_id=str(drink_id),
        drink_name=drink_name,
        drink_image_url=drink_image_url,
        drink_type=drink_type.value,
    )

    actual = drink_application_service.create_drink(input_dto)
    expected = CreateDrinkOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_create_drink_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.add.side_effect = ResourceAlreadyExistError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)
    input_dto = CreateDrinkInputDto(
        drink_id=str(drink_id),
        drink_name=drink_name,
        drink_image_url=drink_image_url,
        drink_type=drink_type.value,
    )

    actual = drink_application_service.create_drink(input_dto)
    expected = FailedOutputDto(type="Resource Conflict Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_update_drink_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = UpdateDrinkInputDto(
        drink_id=str(drink_id),
        drink_name="Tequila",
        drink_image_url="tequila image url",
        drink_type=DrinkType.LIQUOR.value,
        avg_rating=float(DrinkRating(value=3.65)),
        num_of_reviews=10,
        num_of_wish=20,
    )

    actual = drink_application_service.update_drink(input_dto)
    expected = UpdateDrinkOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_update_drink_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.update.side_effect = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = UpdateDrinkInputDto(
        drink_id=str(drink_id),
        drink_name="Tequila",
        drink_image_url="tequila image url",
        drink_type=DrinkType.LIQUOR.value,
        avg_rating=float(DrinkRating(value=3.65)),
        num_of_reviews=10,
        num_of_wish=20,
    )

    actual = drink_application_service.update_drink(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_delete_drink_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.delete_by_drink_id.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkInputDto(drink_id=str(drink_id))

    actual = drink_application_service.delete_drink(input_dto)
    expected = DeleteDrinkOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_delete_drink_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.delete_by_drink_id.side_effect = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkInputDto(drink_id=str(drink_id))

    actual = drink_application_service.delete_drink(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_add_drink_review_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = AddDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5)

    actual = drink_application_service.add_drink_review(input_dto)
    expected = AddDrinkReviewOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_add_drink_review_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.side_effect = ResourceNotFoundError()
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = AddDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5)

    actual = drink_application_service.add_drink_review(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected

    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_repository_mock.update.return_value = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = AddDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5)

    actual = drink_application_service.add_drink_review(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_update_drink_review_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = UpdateDrinkReviewInputDto(drink_id=str(drink_id), old_drink_rating=5, new_drink_rating=4)

    actual = drink_application_service.update_drink_review(input_dto)
    expected = UpdateDrinkReviewOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_update_drink_review_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = None
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = UpdateDrinkReviewInputDto(drink_id=str(drink_id), old_drink_rating=5, new_drink_rating=4)

    actual = drink_application_service.update_drink_review(input_dto)
    expected = FailedOutputDto(
        type="Resource Not Found Error", message="a9a94653-eede-5172-bd44-55653d0dc908의 술을 찾을 수 없습니다."
    )
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_delete_drink_review_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5)

    actual = drink_application_service.delete_drink_review(input_dto)
    expected = DeleteDrinkReviewOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_delete_drink_review_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.side_effect = ResourceNotFoundError()
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5)

    actual = drink_application_service.delete_drink_review(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected

    drink_repository_mock.find_by_drink_id.return_value = None
    drink_repository_mock.update.side_effect = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5)

    actual = drink_application_service.delete_drink_review(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_add_drink_wish_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = AddDrinkWishInputDto(drink_id=str(drink_id))
    actual = drink_application_service.add_drink_wish(input_dto)
    expected = AddDrinkWishOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_add_drink_wish_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.side_effect = ResourceNotFoundError()
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = AddDrinkWishInputDto(drink_id=str(drink_id))
    actual = drink_application_service.add_drink_wish(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected

    drink_repository_mock.find_by_drink_id.return_value = None
    drink_repository_mock.update.side_effect = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = AddDrinkWishInputDto(drink_id=str(drink_id))
    actual = drink_application_service.add_drink_wish(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_delete_drink_wish_success(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.return_value = Drink(
        id=drink_id, name=drink_name, image_url=drink_image_url, type=drink_type
    )
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkWishInputDto(drink_id=str(drink_id))
    actual = drink_application_service.delete_drink_wish(input_dto)
    expected = DeleteDrinkWishOutputDto()
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url, drink_type", drink_data)
def test_delete_drink_wish_fail(
    drink_repository_mock,
    drink_id,
    drink_name,
    drink_image_url,
    drink_type,
):
    drink_repository_mock.find_by_drink_id.side_effect = ResourceNotFoundError()
    drink_repository_mock.update.return_value = None
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkWishInputDto(drink_id=str(drink_id))
    actual = drink_application_service.delete_drink_wish(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected

    drink_repository_mock.find_by_drink_id.return_value = None
    drink_repository_mock.update.side_effect = ResourceNotFoundError()
    drink_application_service = DrinkApplicationService(drink_repository=drink_repository_mock)

    input_dto = DeleteDrinkWishInputDto(drink_id=str(drink_id))
    actual = drink_application_service.delete_drink_wish(input_dto)
    expected = FailedOutputDto(type="Resource Not Found Error", message="")
    assert actual == expected
