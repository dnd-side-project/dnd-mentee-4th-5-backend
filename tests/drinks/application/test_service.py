import uuid

import pytest
from drinks.application.dtos import (
    CreateDrinkInputDto,
    DeleteDrinkInputDto,
    FindDrinkInputDto,
    FindDrinkOutputDto,
    UpdateDrinkInputDto,
    AddDrinkReviewInputDto,
    DeleteDrinkReviewInputDto,
)
from drinks.application.service import DrinkApplicationService
from drinks.domain.entities import Drink
from drinks.domain.value_objects import DrinkRating
from drinks.infra_structure.in_memory_repository import InMemoryDrinkRepository
from shared_kernel.application.dtos import FailedOutputDto


@pytest.fixture
def drink_repository():
    return InMemoryDrinkRepository()


@pytest.fixture
def drink_application_service(drink_repository):
    return DrinkApplicationService(drink_repository=drink_repository)


drink_data = [(uuid.uuid5(uuid.NAMESPACE_DNS, "drink_id"), "Martini", "image_url")]


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url", drink_data)
def test_find_drink(drink_application_service, drink_repository, drink_id, drink_name, drink_image_url):
    drink_repository.add(Drink(id=drink_id, name=drink_name, image_url=drink_image_url))

    input_dto = FindDrinkInputDto(drink_id=str(drink_id))
    actual = drink_application_service.find_drink(input_dto)
    expected = FindDrinkOutputDto(
        drink_id=str(drink_id),
        drink_name=drink_name,
        drink_image_url=drink_image_url,
        avg_rating=float(DrinkRating()),
        num_of_reviews=0,
    )
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url", drink_data)
def test_create_drink(drink_application_service, drink_repository, drink_id, drink_name, drink_image_url):
    input_dto = CreateDrinkInputDto(drink_id=str(drink_id), drink_name=drink_name, drink_image_url=drink_image_url)
    drink_application_service.create_drink(input_dto)

    actual = drink_repository.find_all()
    expected = [
        Drink(
            id=drink_id,
            name=drink_name,
            image_url=drink_image_url,
            avg_rating=DrinkRating(),
            num_of_reviews=0,
        )
    ]
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url", drink_data)
def test_update_drink(drink_application_service, drink_repository, drink_id, drink_name, drink_image_url):
    drink_repository.add(Drink(id=drink_id, name=drink_name, image_url=drink_image_url))

    input_dto = UpdateDrinkInputDto(
        drink_id=str(drink_id),
        drink_name="Tequila",
        drink_image_url="diff image url",
    )
    drink_application_service.update_drink(input_dto)

    actual = drink_repository.find_by_drink_id(drink_id=drink_id)
    expected = Drink(
        id=str(drink_id),
        name="Tequila",
        image_url="diff image url",
    )
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url", drink_data)
def test_delete_drink(drink_application_service, drink_repository, drink_id, drink_name, drink_image_url):
    drink_repository.add(Drink(id=drink_id, name=drink_name, image_url=drink_image_url))

    input_dto = DeleteDrinkInputDto(drink_id=str(drink_id))
    drink_application_service.delete_drink(input_dto)

    actual = drink_repository.find_by_drink_id(drink_id=drink_id)
    expected = None
    assert actual == expected

    # Check delete drink when drink in-memory repo is Empty
    output_dto = drink_application_service.delete_drink(input_dto)
    assert output_dto == FailedOutputDto.build_resource_error(f"{drink_id}의 술 찾지 못했습니다.")


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url", drink_data)
def test_add_drink_review(drink_application_service, drink_repository, drink_id, drink_name, drink_image_url):
    drink_repository.add(
        Drink(
            id=drink_id,
            name=drink_name,
            image_url=drink_image_url,
            avg_rating=DrinkRating(value=3.7),
            num_of_reviews=4,
        )
    )

    input_dto = AddDrinkReviewInputDto(drink_id=drink_id, drink_rating=5)
    drink_application_service.add_drink_reviews(input_dto)

    actual = drink_repository.find_all()
    expected = Drink(
        id=drink_id,
        name=drink_name,
        image_url=drink_image_url,
        avg_rating=DrinkRating(value=3.96),
        num_of_reviews=5,
    )
    assert actual == expected


@pytest.mark.parametrize("drink_id, drink_name, drink_image_url", drink_data)
def test_delete_drink_review(drink_application_service, drink_repository, drink_id, drink_name, drink_image_url):
    drink_repository.add(
        Drink(
            id=drink_id,
            name=drink_name,
            image_url=drink_image_url,
            avg_rating=DrinkRating(value=3.96),
            num_of_reviews=5,
        )
    )

    input_dto = DeleteDrinkReviewInputDto(drink_id=str(drink_id), drink_rating=5, review_update_type="delete")
    drink_application_service.delete_drink_reviews(input_dto)

    actual = drink_repository.find_all()
    expected = Drink(
        id=drink_id,
        name=drink_name,
        image_url=drink_image_url,
        avg_rating=DrinkRating(value=3.7),
        num_of_reviews=4,
    )
    assert actual == expected
