from abc import ABCMeta, abstractmethod
from typing import List, Optional

from users.domain.entities import User
from users.domain.value_objects import UserId


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> List[User]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UserId) -> User:
        pass

    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete_by_user_id(self, user_id: UserId) -> None:
        pass
