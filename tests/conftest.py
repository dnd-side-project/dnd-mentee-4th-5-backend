from fastapi.testclient import TestClient
from main import app
from pytest import fixture


@fixture
def client():
    return TestClient(app)
