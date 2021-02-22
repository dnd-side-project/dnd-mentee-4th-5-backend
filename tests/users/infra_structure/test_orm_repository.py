import pytest

from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from users.domain.entities import User
from shared_kernel.domain.value_objects import UserId, UserName
from users.infra_structure.orm_models import UserOrm
from users.infra_structure.orm_repository import OrmUserRepository


@pytest.fixture(scope="session", autouse=True)
def setup(database):
    with database.session() as session:
        session.execute("DELETE FROM user;")
        session.execute(
            "INSERT INTO user(id, name, description, password, image_url) VALUES "
            "('heumsi', 'heumsi', 'hi, I am heumsi', '1234', ''), "
            "('joon', 'joon', 'hello, I am joon', '4321', '')"
        )
        session.commit()


@pytest.fixture(scope="module", autouse=True)
def setup(database):
    with database.session() as session:
        session.query(UserOrm).delete()
        session.add_all(
            [
                UserOrm.from_user(
                    User(
                        id=UserId(value="heumsi"),
                        name=UserName(value="heumsi"),
                        description="hi, I am heumsi",
                        password="1234",
                        image_url="",
                    )
                ),
                UserOrm.from_user(
                    User(
                        id=UserId(value="joon"),
                        name=UserName(value="joon"),
                        description="hello, I am joon",
                        password="4321",
                        image_url="",
                    )
                ),
            ]
        )
        session.commit()


@pytest.fixture(scope="function")
def orm_user_repository(database):
    return OrmUserRepository(session_factory=database.session)


def test_find_all(orm_user_repository):
    actual = orm_user_repository.find_all()
    expected = [
        User(
            id=UserId(value="heumsi"),
            name=UserName(value="heumsi"),
            description="hi, I am heumsi",
            password="1234",
            image_url="",
        ),
        User(
            id=UserId(value="joon"),
            name=UserName(value="joon"),
            description="hello, I am joon",
            password="4321",
            image_url="",
        ),
    ]
    assert actual == expected


def test_find_by_user_id(orm_user_repository):
    actual = orm_user_repository.find_by_user_id(user_id=UserId(value="heumsi"))
    expected = User(
        id=UserId(value="heumsi"),
        name=UserName(value="heumsi"),
        description="hi, I am heumsi",
        password="1234",
        image_url="",
    )
    assert actual == expected

    with pytest.raises(ResourceNotFoundError):
        orm_user_repository.find_by_user_id(user_id=UserId(value="not exist user"))


def test_add(orm_user_repository):
    orm_user_repository.add(user=User(id=UserId(value="siheum"), name=UserName(value="siheum"), password="1234"))
    actual = orm_user_repository.find_by_user_id(user_id=UserId(value="siheum"))
    expected = User(
        id=UserId(value="siheum"),
        name=UserName(value="siheum"),
        description="",
        password="1234",
        image_url="",
    )
    assert actual == expected

    with pytest.raises(ResourceAlreadyExistError):
        orm_user_repository.add(
            user=User(
                id=UserId(value="siheum"),
                name=UserName(value="siheum"),
                password="1234",
            )
        )


def test_update(orm_user_repository):
    orm_user_repository.update(
        user=User(
            id=UserId(value="heumsi"),
            name=UserName(value="heumsi jeon"),
            description="Hi, I'm heumsi jeon!",
            password="1234",
            image_url="",
        )
    )
    actual = orm_user_repository.find_by_user_id(user_id=UserId(value="heumsi"))
    expected = User(
        id=UserId(value="heumsi"),
        name=UserName(value="heumsi jeon"),
        description="Hi, I'm heumsi jeon!",
        password="1234",
        image_url="",
    )
    assert actual == expected

    with pytest.raises(ResourceNotFoundError):
        orm_user_repository.update(
            user=User(
                id=UserId(value="not exist user"),
                name=UserName(value="heumsi jeon"),
                description="Hi, I'm heumsi jeon!",
                password="1234",
                image_url="",
            )
        )


def test_delete(orm_user_repository):
    with pytest.raises(ResourceNotFoundError):
        orm_user_repository.find_by_user_id(user_id=UserId(value="not exist user"))

    orm_user_repository.delete_by_user_id(UserId(value="heumsi"))
    with pytest.raises(ResourceNotFoundError):
        orm_user_repository.find_by_user_id(user_id=UserId(value="heumsi"))
