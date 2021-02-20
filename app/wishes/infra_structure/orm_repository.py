from contextlib import AbstractContextManager
from typing import Callable, List, Optional

from sqlalchemy.orm import Session

from shared_kernel.domain.exceptions import ResourceAlreadyExistError, ResourceNotFoundError
from wishes.domain.entities import Wish
from wishes.domain.repository import WishRepository, QueryParam
from wishes.domain.value_objects import WishId
from wishes.infra_structure.orm_models import WishOrm

"""
ref: https://stackoverflow.com/questions/41305129/sqlalchemy-dynamic-filtering
"""


class OrmWishRepository(WishRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self._session_factory = session_factory

    def find(self, query_param: QueryParam) -> Wish:
        query_param = {attr: value for attr, value in query_param if value}
        with self._session_factory() as session:
            query = session.query(WishOrm)
            wish_orm = query.filter_by(**query_param).first()
            if wish_orm is None:
                raise ResourceNotFoundError(f"해당하는 위시를 찾지 못했습니다.")
            return wish_orm.to_wish()

    def find_all(self, query_param: QueryParam) -> List[Wish]:
        query_param = {attr: value for attr, value in query_param if value}
        with self._session_factory() as session:
            query = session.query(WishOrm)
            wish_orms = query.filter_by(**query_param).all()
            return [wish_orm.to_wish() for wish_orm in wish_orms]

    def add(self, wish: Wish) -> None:
        with self._session_factory() as session:
            wish_orm = session.query(WishOrm).filter(WishOrm.id == str(wish.id)).first()
            if wish_orm is not None:
                raise ResourceAlreadyExistError(f"{str(wish.id)}는 이미 존재하는 위시입니다.")
            wish_orm = WishOrm.from_wish(wish)
            session.add(wish_orm)
            session.commit()

    def delete_by_wish_id(self, wish_id: WishId) -> None:
        with self._session_factory() as session:
            wish_orm = session.query(WishOrm).filter(WishOrm.id == str(wish_id)).first()
            if wish_orm is None:
                raise ResourceNotFoundError(f"{str(wish_id)}의 위시를 찾지 못했습니다.")
            session.delete(wish_orm)
            session.commit()
