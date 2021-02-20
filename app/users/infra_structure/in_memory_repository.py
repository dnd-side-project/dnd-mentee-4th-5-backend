from typing import List, Optional

from shared_kernel.domain.value_objects import UserId
from users.domain.entities import User
from users.domain.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.user_id_to_user = {}

    def find_by_user_id(self, user_id: UserId) -> Optional[User]:
        return self.user_id_to_user.get(str(user_id), None)

    def add(self, user: User) -> None:
        self.user_id_to_user[str(user.id)] = user

    def update(self, user: User) -> None:
        self.user_id_to_user[str(user.id)] = user

    def find_all(self) -> List[User]:
        return list(self.user_id_to_user.values())

    def delete_by_user_id(self, user_id: UserId) -> None:
        self.user_id_to_user.pop(str(user_id), None)
