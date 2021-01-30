import pytest

from users.infra_structure.in_memory_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


def test_post_users(client):
    response = client.post("/users", json={"user_id": "heumsi", "user_name": "heumsi", "hashed_password": "1234"})
    assert response.status_code == 200
