from dependency_injector import containers, providers

from auth.application.service import AuthApplicationService
from reviews.application.service import ReviewApplicationService
from reviews.infra_structure.in_memory_repository import InMemoryReviewRepository
from settings import Settings
from users.application.service import UserApplicationService
from users.infra_structure.in_memory_repository import InMemoryUserRepository
from wishes.application.service import WishApplicationService
from wishes.infra_structure.in_memory_repository import InMemoryWishRepository


class Container(containers.DeclarativeContainer):
    # settings
    settings = providers.Singleton(Settings)

    # repository
    user_repository = providers.Singleton(InMemoryUserRepository)
    review_repository = providers.Singleton(InMemoryReviewRepository)
    wish_repository = providers.Singleton(InMemoryWishRepository)

    # application service
    user_application_service = providers.Singleton(UserApplicationService, user_repository=user_repository)
    auth_application_service = providers.Singleton(
        AuthApplicationService, user_application_service=user_application_service, settings=settings
    )
    review_application_service = providers.Singleton(ReviewApplicationService, review_repository=review_repository)
    wish_application_service = providers.Singleton(WishApplicationService, wish_repository=wish_repository)
