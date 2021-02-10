from auth.external_interface.json_dto import GetTokenJsonRequest


def test_get_token(client):
    response = client.get("/auth/token", json=GetTokenJsonRequest(user_id="heumsi", password="1234").dict())
    assert response.status_code == 404
    assert response.json() == {"error_type": "Resource Error", "message": "heumsi의 유저를 찾지 못했습니다."}

    # TODO: 성공하는 케이스는 어떻게 테스트 코드를 작성할까?
