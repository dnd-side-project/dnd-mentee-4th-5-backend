# import pathlib

import pytest
from starlette.testclient import TestClient

from main import create_app
from shared_kernel.infra_structure.database import Database

# TEST_ROOT_PATH = pathlib.Path(__file__).parent.absolute()

# fixtures for database (testing ORM Repository)
@pytest.fixture(scope="session")
def database():
    database = Database(db_url=f"sqlite:///./db.sqlite3")
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
