from typing import List, Optional

from wishes.domain.entities import Wish
from wishes.domain.repository import QueryParam, WishRepository


class InMemoryWishRepository(WishRepository):
    def __init__(self) -> None:
        self._wishes = []

    def find(self, query_param: QueryParam) -> Optional[Wish]:
        for wish in self._wishes:
            for name, value in query_param:
                if value is None:
                    continue
                if wish.__fields__[name] != value:
                    break
            return wish

    def find_all(self, query_param: QueryParam) -> List[Wish]:
        result = []
        for wish in self._wishes:
            for name, value in query_param:
                if value is None:
                    continue
                if wish.__fields__[name] != value:
                    break
            result.append(wish)
        return result

    def add(self, wish: Wish) -> None:
        self._wishes.append(wish)

    def delete_by_wish_id(self, wish: Wish) -> None:
        self._wishes.remove(wish)
