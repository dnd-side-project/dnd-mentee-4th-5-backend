import pytest
from main import create_app
from shared_kernel.infra_structure.database import Database
from starlette.testclient import TestClient


# fixtures for database (testing ORM Repository)
@pytest.fixture(scope="session")
def database():
    database = Database(db_url=f"postgresql://seokjunhong:@Hse05040!@localhost:5432/jun")
    database.create_database()
    return database


# will be deprecated
@pytest.fixture(scope="session")
def app():
    return create_app()


# will be deprecated
@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)
