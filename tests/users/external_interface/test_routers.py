from users.external_interface.json_dto import (CreateUserJsonRequest,
                                               UpdateUserJsonRequest)


def test_get_users(client):
    # valid request but no resource
    response = client.get("/users/heumsi")
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "heumsi의 유저를 찾지 못했습니다.",
    }

    # valid request
    response = client.post(
        "/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"}
    )
    assert response.status_code == 201

    response = client.get("/users/heumsi")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "heumsi",
        "user_name": "heumsi",
        "description": "",
        "image_url": "",
    }


def test_post_users(client):
    response = client.post(
        "/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"}
    )
    assert response.status_code == 201

    response = client.post(
        "/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"}
    )
    assert response.status_code == 409
    assert response.json() == {
        "error_type": "Resource Conflict Error",
        "message": "heumsi는 이미 존재하는 유저입니다.",
    }


def test_put_users(client):
    # wrong request without header
    response = client.put(
        "/users",
        json=UpdateUserJsonRequest(
            user_name="heumsi", description="시흠입니다.", password="1234"
        ).dict(),
    )
    assert response.status_code == 422

    # wrong request with wrong header value
    response = client.put(
        "/users",
        headers={"access-token": "wrong header value"},
        json=UpdateUserJsonRequest(
            user_name="heumsi", description="시흠입니다.", password="1234"
        ).dict(),
    )
    assert response.status_code == 401
    assert response.json() == {
        "error_type": "Unauthorized Error",
        "message": "올바른 access-token이 아닙니다.",
    }

    # valid request but no resource
    response = client.put(
        "/users",
        headers={
            "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
        },
        json=UpdateUserJsonRequest(
            user_name="heumsi", description="시흠입니다.", password="1234"
        ).dict(),
    )
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "heumsi의 유저를 찾지 못했습니다.",
    }

    # valid request
    response = client.post(
        "/users",
        json=CreateUserJsonRequest(
            user_id="heumsi", user_name="heumsi", password="1234"
        ).dict(),
    )
    assert response.status_code == 201

    response = client.put(
        "/users",
        headers={
            "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
        },
        json=UpdateUserJsonRequest(
            user_name="siheum", description="시흠입니다.", password="1234"
        ).dict(),
    )
    assert response.status_code == 204


def test_delete_users(client):
    # wrong request without header
    response = client.delete(
        "/users",
    )
    assert response.status_code == 422

    # wrong request with wrong header value
    response = client.delete(
        "/users",
        headers={"access-token": "wrong header value"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "error_type": "Unauthorized Error",
        "message": "올바른 access-token이 아닙니다.",
    }

    # valid request but no resource
    response = client.delete(
        "/users",
        headers={
            "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
        },
        json=UpdateUserJsonRequest(
            user_name="heumsi", description="시흠입니다.", password="1234"
        ).dict(),
    )
    assert response.status_code == 404
    assert response.json() == {
        "error_type": "Resource Not Found Error",
        "message": "heumsi의 유저를 찾지 못했습니다.",
    }

    # valid request
    response = client.post(
        "/users",
        json=CreateUserJsonRequest(
            user_id="heumsi", user_name="heumsi", password="1234"
        ).dict(),
    )
    assert response.status_code == 201

    response = client.delete(
        "/users",
        headers={
            "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
        },
    )
    assert response.status_code == 204
