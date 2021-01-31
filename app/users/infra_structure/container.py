from dependency_injector import containers, providers

from users.infra_structure.in_memory_repository import InMemoryUserRepository


class Container(containers.DeclarativeContainer):

    user_repository = providers.Singleton(InMemoryUserRepository)
