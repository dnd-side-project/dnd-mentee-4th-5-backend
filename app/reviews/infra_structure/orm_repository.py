from contextlib import AbstractContextManager
from typing import Callable, List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from reviews.domain.entities import Review
from reviews.domain.repository import QueryParam, ReviewRepository
from reviews.domain.value_objects import OrderType, ReviewRating
from reviews.infra_structure.orm_models import ReviewOrm
from shared_kernel.domain.exceptions import InvalidParamInputError, ResourceAlreadyExistError, ResourceNotFoundError
from shared_kernel.domain.value_objects import DrinkId, ReviewId, UserId


class OrmReviewRepository(ReviewRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self._session_factory = session_factory

    def find(self, query_param: QueryParam) -> Review:
        if not query_param.user_id or not query_param.drink_id:
            raise InvalidParamInputError(
                f"drink_id: {query_param.drink_id} and user_id:{query_param.user_id}에 해당하는 값이 없습니다."
            )
        _query_param = {attr: value for attr, value in query_param if value and not isinstance(value, OrderType)}
        with self._session_factory() as session:
            query = session.query(ReviewOrm)
            review_orm = query.filter_by(**_query_param).first()
            if review_orm is None:
                raise ResourceNotFoundError(f"리뷰를 찾지 못했습니다.")
            return review_orm.to_review()

    def find_all(self, query_param: QueryParam) -> List[Review]:
        if not query_param.user_id and not query_param.drink_id:
            raise InvalidParamInputError(
                f"drink_id: {query_param.drink_id} or user_id:{query_param.user_id}에 해당하는 값이 없습니다."
            )
        _query_param = {attr: value for attr, value in query_param if value and not isinstance(value, OrderType)}
        with self._session_factory() as session:

            order_type = desc(ReviewOrm.updated_at)
            # if order_type == OrderType.LIKE_DESC:
            #     order_type = desc(ReviewOrm.num_likes)
            # elif order_type == OrderType.LIKE_ASC:
            #     order_type = asc(ReviewOrm.num_likes)

            query = session.query(ReviewOrm)
            review_orms = query.filter_by(**_query_param).order_by(order_type).all()

            return [
                Review(
                    id=ReviewId(value=review_orm.id),
                    drink_id=DrinkId(value=review_orm.drink_id),
                    user_id=UserId(value=review_orm.user_id),
                    rating=ReviewRating(value=review_orm.rating),
                    comment=review_orm.comment,
                    created_at=review_orm.created_at,
                    updated_at=review_orm.updated_at,
                )
                for review_orm in review_orms
            ]

    def find_by_review_id(self, review_id: ReviewId) -> Optional[Review]:
        with self._session_factory() as session:
            review_orm = session.query(ReviewOrm).filter(ReviewOrm.id == str(review_id)).first()
            if review_orm is None:
                raise ResourceNotFoundError(f"{str(review_id)}의 리뷰를 찾지 못했습니다.")
            return review_orm.to_review()

    def add(self, review: Review) -> None:
        with self._session_factory() as session:
            review_orm = session.query(ReviewOrm).filter(ReviewOrm.id == str(review.id)).first()
            if review_orm is not None:
                raise ResourceAlreadyExistError(f"{str(review.id)}는 이미 존재하는 리뷰입니다.")

            review_orm = ReviewOrm.from_review(review)
            session.add(review_orm)
            session.commit()

    def update(self, review: Review) -> None:
        with self._session_factory() as session:
            review_orm = session.query(ReviewOrm).filter(ReviewOrm.id == str(review.id)).first()
            if review_orm is None:
                raise ResourceNotFoundError(f"{str(review.id)}의 리뷰를 찾지 못했습니다.")
            review_orm.fetch_review(review)
            session.commit()

    def delete_by_review_id(self, review_id: ReviewId) -> None:
        with self._session_factory() as session:
            review_orm = session.query(ReviewOrm).filter(ReviewOrm.id == str(review_id)).first()
            if review_orm is None:
                raise ResourceNotFoundError(f"{str(review_id)}의 리뷰를 찾지 못했습니다.")
            session.delete(review_orm)
            session.commit()
