from fastapi.testclient import TestClient
from main import create_app
from pytest import fixture


@fixture(scope="function")
def client():
    return TestClient(create_app())
