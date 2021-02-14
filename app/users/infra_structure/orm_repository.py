from contextlib import AbstractContextManager
from typing import List, Callable

from sqlalchemy.orm import Session

from shared_kernel.infra_structure.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from users.domain.entities import User
from users.domain.repository import UserRepository
from users.domain.value_objects import UserId, UserName
from users.infra_structure.orm_models import UserOrm


class OrmUserRepository(UserRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self._session_factory = session_factory

    def find_all(self) -> List[User]:
        with self._session_factory() as session:
            user_orms = session.query(UserOrm).all()
            return [
                User(
                    id=UserId(value=user_orm.id),
                    name=UserName(value=user_orm.name),
                    description=user_orm.description,
                    password=user_orm.password,
                    image_url=user_orm.image_url,
                )
                for user_orm in user_orms
            ]

    def find_by_user_id(self, user_id: UserId) -> User:
        with self._session_factory() as session:
            user_orm = session.query(UserOrm).filter(UserOrm.id == str(user_id)).first()
            if user_orm is None:
                raise ResourceNotFoundError(f"{str(user_id)}의 유저를 찾지 못했습니다.")
            return user_orm.to_user()

    def add(self, user: User) -> None:
        with self._session_factory() as session:
            user_orm = session.query(UserOrm).filter(UserOrm.id == str(user.id)).first()
            if user_orm is not None:
                raise ResourceAlreadyExistError(f"{str(user.id)}는 이미 존재하는 유저입니다.")
            user_orm = UserOrm.from_user(user)
            session.add(user_orm)
            session.commit()

    def update(self, user: User) -> None:
        with self._session_factory() as session:
            user_orm = session.query(UserOrm).filter(UserOrm.id == str(user.id)).first()
            if user_orm is None:
                raise ResourceNotFoundError(f"{str(user.id)}의 유저를 찾지 못했습니다.")
            user_orm.fetch_user(user)
            session.commit()

    def delete_by_user_id(self, user_id: UserId) -> None:
        pass
