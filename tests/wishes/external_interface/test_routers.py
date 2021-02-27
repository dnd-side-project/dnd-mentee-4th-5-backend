from unittest import mock

import pytest

from auth.application.dtos import GetTokenDataOutputDto
from auth.application.service import AuthApplicationService
from wishes.application.dto import FindWishesOutputDto, CreateWishOutputDto, DeleteWishOutputDto
from wishes.application.service import WishApplicationService


@pytest.fixture(scope="function")
def wish_application_service_mock():
    return mock.Mock(spec=WishApplicationService)


@pytest.fixture(scope="function")
def auth_application_service_mock():
    m = mock.Mock(spec=AuthApplicationService)
    m.get_token_data.return_value = GetTokenDataOutputDto(user_id="heumsi")
    return m


def test_get_wishes_success(wish_application_service_mock, client, app):
    wish_application_service_mock.find_wishes.return_value = FindWishesOutputDto(
        items=[FindWishesOutputDto.Item(id="wish_id", user_id="heumsi", drink_id="drink_id", created_at=1613884133)]
    )

    # get by user_id
    with app.container.wish_application_service.override(wish_application_service_mock):
        response = client.get("/wishes?user_id=heumsi")
    assert response.status_code == 200
    assert response.json() == [
        {"id": "wish_id", "user_id": "heumsi", "drink_id": "heumsi", "created_at": 1613884133.0},
    ]

    # get by drink_id
    with app.container.wish_application_service.override(wish_application_service_mock):
        response = client.get("/wishes?drink_id=drink_id")
    assert response.status_code == 200
    assert response.json() == [
        {"id": "wish_id", "user_id": "heumsi", "drink_id": "heumsi", "created_at": 1613884133.0},
    ]


def test_create_wish_success(auth_application_service_mock, wish_application_service_mock, client, app):
    wish_application_service_mock.create_wish.return_value = CreateWishOutputDto(
        id="wish_id", user_id="heumsi", drink_id="drink_id", created_at=1613884133
    )

    with app.container.auth_application_service.override(auth_application_service_mock):
        with app.container.wish_application_service.override(wish_application_service_mock):
            response = client.post("/wishes/drink_id", headers={"access-token": "dump_value"})
    assert response.status_code == 201
    assert response.json() == {"user_id": "heumsi", "drink_id": "drink_id", "created_at": 1613884133.0}


def test_delete_wish_success(auth_application_service_mock, wish_application_service_mock, client, app):
    wish_application_service_mock.delete_wish.return_value = DeleteWishOutputDto()

    with app.container.auth_application_service.override(auth_application_service_mock):
        with app.container.wish_application_service.override(wish_application_service_mock):
            response = client.delete("/wishes/drink_id", headers={"access-token": "dump_value"})
    assert response.status_code == 204
