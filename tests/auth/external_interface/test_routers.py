def test_get_token(client):
    response = client.get("/auth/token", json={"user_id": "heumsi", "password": "1234"})
    assert response.status_code == 422
    assert response.json() == {"message": "heumsi의 유저를 찾지 못했습니다."}

    # TODO: 성공하는 케이스는 어떻게 테스트 코드를 작성할까?
