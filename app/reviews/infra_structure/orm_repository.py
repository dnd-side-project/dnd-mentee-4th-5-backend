from contextlib import AbstractContextManager
from typing import Callable, List, Optional

from reviews.domain.entities import Review
from reviews.domain.repository import QueryParam, ReviewRepository
from reviews.domain.value_objects import (DrinkId, OrderType, ReviewId,
                                          ReviewRating, UserId)
from reviews.infra_structure.orm_models import ReviewOrm
from shared_kernel.domain.exceptions import (InvalidParamInputError,
                                             ResourceAlreadyExistError,
                                             ResourceNotFoundError)
from sqlalchemy.orm import Session


class OrmReviewRepository(ReviewRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self._session_factory = session_factory

    def find_all(self, query_param: QueryParam, order: OrderType = OrderType.LIKE_DESC) -> List[Review]:
        with self._session_factory as session:
            if not QueryParam.user_id and not QueryParam.drink_id:
                review_orms = session.query(ReviewOrm).all()
            elif not QueryParam.user_id:
                review_orms = session.query(ReviewOrm).filter(ReviewOrm.drink_id == QueryParam.drink_id)
            else:
                review_orms = session.query(ReviewOrm).filter(ReviewOrm.user_id == QueryParam.user_id)
            return [
                Review(
                    id=ReviewId(value=review_orm.id),
                    drink_id=DrinkId(value=review_orm.drink_id),
                    user_id=UserId(value=review_orm.user_id),
                    rating=ReviewRating(value=review_orms.rating),
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

    def find_by_drink_id_user_id(self, query_param: QueryParam) -> Optional[Review]:
        with self._session_factory() as session:
            if not QueryParam.user_id or not QueryParam.drink_id:
                raise InvalidParamInputError(f"술: {QueryParam.drink_id}, 유저: {QueryParam.user_id}에 해당하는 값이 없습니다.")
            else:
                review_orm = (
                    session.query(ReviewOrm)
                    .filter(ReviewOrm.drink_id == QueryParam.drink_id, ReviewOrm.user_id == QueryParam.user_id)
                    .first()
                )
            if review_orm is None:
                raise ResourceNotFoundError(f"술: {QueryParam.drink_id}, 유저: {QueryParam.user_id} 리뷰를 찾지 못했습니다.")
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
