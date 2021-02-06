from dependency_injector import containers, providers
from reviews.infra_structure.in_memory_repository import InMemoryReviewRepository


class Container(containers.DeclarativeContainer):
    review_repository = providers.Singleton(InMemoryReviewRepository)
