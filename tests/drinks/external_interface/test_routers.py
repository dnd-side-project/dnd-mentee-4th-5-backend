import uuid
from unittest import mock

from drinks.application.dtos import FindDrinksOutputDto, CreateDrinkOutputDto
from drinks.application.service import DrinkApplicationService
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.value_objects import DrinkId


def test_post_drinks(client, app):
    application_service_mock = mock.Mock(spec=DrinkApplicationService)
    application_service_mock.create_drink.return_value = FailedOutputDto.build_resource_conflict_error()

    with app.container.drink_application_service.override(application_service_mock):
        response = client.post(
            "/drinks",
            json={
                "drink_id": str(DrinkId(value=uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_1"))),
                "drink_name": "wine_1",
                "drink_image_url": "picture_wine_1",
                "drink_type": "wine",
            },
        )

        assert response.status_code == 409
        assert response.json() == {
            "error_type": "Resource Conflict Error",
            "message": "",
        }

    application_service_mock.create_drink.return_value = CreateDrinkOutputDto()
    with app.container.drink_application_service.override(application_service_mock):
        response = client.post(
            "/drinks",
            json={
                "drink_id": str(DrinkId(value=uuid.uuid5(uuid.NAMESPACE_DNS, "drink_num_1"))),
                "drink_name": "wine_1",
                "drink_image_url": "picture_wine_1",
                "drink_type": "wine",
            },
        )
        assert response.status_code == 201


def test_get_drinks(client, app):
    application_service_mock = mock.Mock(spec=DrinkApplicationService)
    application_service_mock.find_drinks.return_value = FindDrinksOutputDto(
        items=[
            FindDrinksOutputDto.Item(
                drink_id="drink_id_uuid",
                drink_name="drink_name",
                drink_image_url="drink_image_url",
                drink_type="drink_type",
                avg_rating=4.5,
                num_of_reviews=2,
                num_of_wish=2,
            ),
            FindDrinksOutputDto.Item(
                drink_id="drink_id_uuid2",
                drink_name="drink_name2",
                drink_image_url="drink_image_url2",
                drink_type="drink_type2",
                avg_rating=3.5,
                num_of_reviews=4,
                num_of_wish=4,
            ),
        ]
    )
    with app.container.drink_application_service.override(application_service_mock):
        response = client.get("/drinks?type=wine&filter=review&order=descending")
        assert response.status_code == 200
        assert response.json() == [
            {
                "drink_id": "drink_id_uuid",
                "name": "drink_name",
                "image_url": "drink_image_url",
                "type": "drink_type",
                "avg_rating": 4.5,
                "num_of_reviews": 2,
                "num_of_wish": 2,
            },
            {
                "drink_id": "drink_id_uuid2",
                "name": "drink_name2",
                "image_url": "drink_image_url2",
                "type": "drink_type2",
                "avg_rating": 3.5,
                "num_of_reviews": 4,
                "num_of_wish": 4,
            },
        ]
