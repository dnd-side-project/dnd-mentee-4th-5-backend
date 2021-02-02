from dependency_injector import containers, providers

from auth.application.service import AuthApplicationService
from users.application.service import UserApplicationService
from users.infra_structure.in_memory_repository import InMemoryUserRepository


class Container(containers.DeclarativeContainer):

    # repository
    user_repository = providers.Singleton(InMemoryUserRepository)

    # application service
    user_application_service = providers.Singleton(UserApplicationService, user_repository=user_repository)
    auth_application_service = providers.Singleton(
        AuthApplicationService, user_application_service=user_application_service
    )
