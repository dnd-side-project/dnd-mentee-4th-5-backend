from unittest import mock

import pytest

from shared_kernel.application.dtos import FailedOutputDto
from users.application.dtos import FindUserOutputDto, CreateUserOutputDto, UpdateUserOutputDto, DeleteUserOutputDto
from users.application.service import UserApplicationService


@pytest.fixture(scope="function")
def user_application_service_mock():
    return mock.Mock(spec=UserApplicationService)


@pytest.fixture(scope="function")
def auth_application_service_mock():
    return mock.Mock()


def test_get_users_success(user_application_service_mock, client, app):
    user_application_service_mock.find_user.return_value = FindUserOutputDto(
        user_id="heumsi", user_name="heumsi", description="", image_url=""
    )

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.get("/users/heumsi")
    assert response.status_code == 200
    assert response.json() == {"user_id": "heumsi", "user_name": "heumsi", "description": "", "image_url": ""}


def test_get_users_fail(user_application_service_mock, client, app):
    user_application_service_mock.find_user.return_value = FailedOutputDto.build_resource_not_found_error()

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.get("/users/heumsi")
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "",
    }


def test_post_users_success(user_application_service_mock, client, app):
    user_application_service_mock.create_user.return_value = CreateUserOutputDto(
        user_id="heumsi", user_name="heumsi", description="", image_url=""
    )

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.post("/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"})
    assert response.status_code == 201
    assert response.json() == {"user_id": "heumsi", "user_name": "heumsi", "description": "", "image_url": ""}


def test_post_users_fail(user_application_service_mock, client, app):
    user_application_service_mock.create_user.return_value = FailedOutputDto(
        type="Resource Conflict Error", message="heumsi는 이미 존재하는 유저입니다."
    )
    with app.container.user_application_service.override(user_application_service_mock):
        response = client.post("/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"})
    assert response.status_code == 409
    assert response.json() == {"error_type": "Resource Conflict Error", "message": "heumsi는 이미 존재하는 유저입니다."}


def test_put_users_fail_with_not_exist_user(user_application_service_mock, client, app):
    user_application_service_mock.update_user.return_value = FailedOutputDto(
        type="Resource Not Found Error", message="heumsi의 유저를 찾지 못했습니다."
    )

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.put(
            "/users",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
            json={"user_name": "heumsi", "description": "시흠입니다.", "password": "1234"},
        )
    assert response.status_code == 404
    assert response.json() == {"error_type": "Resource Not Found Error", "message": "heumsi의 유저를 찾지 못했습니다."}


def test_put_users_success(user_application_service_mock, client, app):
    user_application_service_mock.update_user.return_value = UpdateUserOutputDto()

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.put(
            "/users",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
            json={"user_name": "heumsi", "description": "Hi, I'm heumsi", "password": "1234"},
        )
    assert response.status_code == 204


def test_delete_users_success(user_application_service_mock, client, app):
    user_application_service_mock.delete_user.return_value = DeleteUserOutputDto()

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.delete(
            "/users",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
        )
    assert response.status_code == 204


def test_delete_users_fail(user_application_service_mock, client, app):
    user_application_service_mock.delete_user.return_value = FailedOutputDto.build_resource_not_found_error(
        message="heumsi의 유저를 찾지 못했습니다."
    )

    with app.container.user_application_service.override(user_application_service_mock):
        response = client.delete(
            "/users",
            headers={
                "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
            },
        )
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "heumsi의 유저를 찾지 못했습니다.",
    }
