from typing import List, Optional
from uuid import UUID

from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository
from drinks.domain.value_objects import DrinkType, FilterType, OrderType


class InMemoryDrinkRepository(DrinkRepository):
    def __init__(self) -> None:
        self.drink_id_to_drink = {}

    # only for test purpose
    def find_all(self) -> List[Drink]:
        return list(self.drink_id_to_drink.values())

    # def find_all(self, drink_type: DrinkType, filter_type: FilterType, order: OrderType) -> List[Drink]:
    #     return list(self.drink_id_to_drink.values())

    def find_by_drink_id(self, drink_id: UUID) -> Optional[Drink]:
        return self.drink_id_to_drink.get(str(drink_id), None)

    def add(self, drink: Drink) -> None:
        self.drink_id_to_drink[str(drink.id)] = drink

    def update(self, drink: Drink) -> None:
        self.drink_id_to_drink[str(drink.id)] = drink

    def delete_by_drink_id(self, drink_id: UUID) -> None:
        self.drink_id_to_drink.pop(str(drink_id), None)
