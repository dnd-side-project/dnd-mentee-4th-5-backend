def test_post_users(client):
    response = client.post("/users", json={"user_id": "heumsi", "user_name": "heumsi", "hashed_password": "1234"})
    assert response.status_code == 200
