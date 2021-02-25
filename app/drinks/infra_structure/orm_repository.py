from contextlib import AbstractContextManager
from typing import Optional, List, Callable
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository, QueryParam
from drinks.domain.value_objects import OrderType, FilterType, DrinkType
from drinks.infra_structure.orm_models import DrinkOrm
from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from shared_kernel.domain.value_objects import DrinkId


class OrmDrinkRepository(DrinkRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self._session_factory = session_factory

    def find_by_drink_id(self, drink_id: DrinkId) -> Optional[Drink]:
        with self._session_factory() as session:
            drink_orm = session.query(DrinkOrm).filter(DrinkOrm.id == str(drink_id)).first()
            if drink_orm is None:
                raise ResourceNotFoundError(f"{str(drink_id)}의 리뷰를 찾지 못했습니다.")
            return drink_orm.to_drink()

    def find_all(self, query_param: QueryParam) -> List[Drink]:
        with self._session_factory() as session:
            order_filter = DrinkOrm.num_of_reviews
            if query_param.filter == FilterType.RATING:
                order_filter = DrinkOrm.avg_rating
            elif query_param.filter == FilterType.WISH:
                order_filter = DrinkOrm.num_of_wish

            order_type = desc(order_filter)
            if order_type == OrderType.ASC:
                order_type = asc(order_filter)

            query = session.query(DrinkOrm)
            if query_param.type == DrinkType.ALL:
                drink_orms = query.order_by(order_type).all()
            else:
                drink_orms = query.filter(DrinkOrm.type == query_param.type.value).order_by(order_type).all()

            return [drink_orm.to_drink() for drink_orm in drink_orms]

    def add(self, drink: Drink) -> None:
        with self._session_factory() as session:
            drink_orm = session.query(DrinkOrm).filter(DrinkOrm.id == str(drink.id)).first()
            if drink_orm is not None:
                raise ResourceAlreadyExistError(f"{str(drink.id)}는 이미 존재하는 리뷰입니다.")

            drink_orm = DrinkOrm.from_drink(drink)
            session.add(drink_orm)
            session.commit()

    def update(self, drink: Drink) -> None:
        with self._session_factory() as session:
            drink_orm = session.query(DrinkOrm).filter(DrinkOrm.id == str(drink.id)).first()

            if drink_orm is None:
                raise ResourceNotFoundError(f"{str(drink.id)}의 리뷰를 찾지 못했습니다.")

            drink_orm.fetch_drink(drink)
            session.commit()

    def delete_by_drink_id(self, drink_id: DrinkId) -> None:
        with self._session_factory() as session:
            drink_orm = session.query(DrinkOrm).filter(DrinkOrm.id == str(drink_id)).first()
            if drink_orm is None:
                raise ResourceNotFoundError(f"{str(drink_id)}의 리뷰를 찾지 못했습니다.")
            session.delete(drink_orm)
            session.commit()
