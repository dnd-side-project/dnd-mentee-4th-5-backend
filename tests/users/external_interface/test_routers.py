def test_post_users(client):
    response = client.post("/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"})
    assert response.status_code == 201

    response = client.post("/users", json={"user_id": "heumsi", "user_name": "heumsi", "password": "1234"})
    assert response.status_code == 422
    assert response.json() == {"message": "heumsi는 이미 존재하는 유저입니다."}
