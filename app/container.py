from auth.application.service import AuthApplicationService
from shared_kernel.infra_structure.database import Database
from dependency_injector import containers, providers
from drinks.application.service import DrinkApplicationService
from drinks.infra_structure.in_memory_repository import InMemoryDrinkRepository
from reviews.application.service import ReviewApplicationService
from reviews.infra_structure.in_memory_repository import InMemoryReviewRepository
from users.application.service import UserApplicationService
from users.infra_structure.orm_repository import OrmUserRepository
from wishes.application.service import WishApplicationService
from wishes.infra_structure.in_memory_repository import InMemoryWishRepository
from wishes.infra_structure.orm_repository import OrmWishRepository


class Container(containers.DeclarativeContainer):
    # settings
    settings = providers.Configuration()

    # database
    db = providers.Singleton(Database, db_url=settings.DB_URL)

    # repository
    user_repository = providers.Singleton(OrmUserRepository, session_factory=db.provided.session)
    review_repository = providers.Singleton(InMemoryReviewRepository)
    wish_repository = providers.Singleton(OrmWishRepository, session_factory=db.provided.session)
    drink_repository = providers.Singleton(InMemoryDrinkRepository)

    # application service
    user_application_service = providers.Singleton(UserApplicationService, user_repository=user_repository)
    auth_application_service = providers.Singleton(
        AuthApplicationService,
        user_application_service=user_application_service,
        jwt_secret_key=settings.JWT_SECRET_KEY,
        jwt_algorithm=settings.JWT_ALGORITHM,
    )
    review_application_service = providers.Singleton(ReviewApplicationService, review_repository=review_repository)
    wish_application_service = providers.Singleton(WishApplicationService, wish_repository=wish_repository)
    drink_application_service = providers.Singleton(DrinkApplicationService, drink_repository=drink_repository)
