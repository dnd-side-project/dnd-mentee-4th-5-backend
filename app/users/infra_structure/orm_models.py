from sqlalchemy import Column, String

from shared_kernel.domain.value_objects import UserId, UserName
from shared_kernel.infra_structure.database import Base
from users.domain.entities import User


class UserOrm(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default="", nullable=False)
    password = Column(String, nullable=False)
    image_url = Column(String, default="", nullable=False)

    @classmethod
    def from_user(cls, user: User) -> "UserOrm":
        return UserOrm(
            id=str(user.id),
            name=str(user.name),
            description=user.description,
            password=user.password,
            image_url=user.image_url,
        )

    def fetch_user(self, user: User) -> None:
        self.name = str(user.name)
        self.description = user.description
        self.password = user.password
        self.image_url = user.image_url

    def to_user(self) -> User:
        return User(
            id=UserId(value=self.id),
            name=UserName(value=self.name),
            description=self.description,
            password=self.password,
            image_url=self.image_url,
        )
