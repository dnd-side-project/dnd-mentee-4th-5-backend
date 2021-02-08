from users.external_interface.json_dto import UpdateUserJsonRequest


def test_post_users(client):
    response = client.post(
        "/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"}
    )
    assert response.status_code == 201

    response = client.post(
        "/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"}
    )
    assert response.status_code == 422
    assert response.json() == {"message": "heumsi는 이미 존재하는 유저입니다."}


def test_put_users(client):
    # without header
    response = client.put(
        "/users",
        json=UpdateUserJsonRequest(user_id="heumsi", user_name="heumsi", description="시흠입니다.", password="1234").dict(),
    )
    assert response.status_code == 422

    # wrong header value
    response = client.put(
        "/users",
        headers={"access-token": "wrong header value"},
        json=UpdateUserJsonRequest(user_id="heumsi", user_name="heumsi", description="시흠입니다.", password="1234").dict(),
    )
    assert response.status_code == 401
    assert response.json() == {"message": "올바른 access-token이 아닙니다."}

    # not
    response = client.put(
        "/users",
        headers={
            "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiaGV1bXNpIn0.OuFWvZ07CwSzR1j7I-wxFHweVb6sB8_U2LezYL7nz3I"
        },
        json=UpdateUserJsonRequest(user_id="heumsi", user_name="heumsi", description="시흠입니다.", password="1234").dict(),
    )
    assert response.status_code == 401
    assert response.json() == {"message": "올바른 access-token이 아닙니다."}
    assert False
