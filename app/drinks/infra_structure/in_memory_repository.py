from typing import List, Optional

from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository
from drinks.domain.value_objects import (DrinkId, DrinkType, FilterType,
                                         OrderType)


class InMemoryDrinkRepository(DrinkRepository):
    def __init__(self) -> None:
        self.drink_id_to_drink = {}

    # only for test purpose
    def find_all_simple(self) -> List[Drink]:
        return list(self.drink_id_to_drink.values())

    def find_all(self, drink_type: DrinkType, filter_type: FilterType, order: OrderType) -> List[Drink]:
        drinks = list(self.drink_id_to_drink.values())
        drinks_typed = [drink for drink in drinks if drink.type == drink_type]

        drinks_filtered_in_order = []
        order_type = order != OrderType.DESC
        if filter_type == filter_type.REVIEW:
            drinks_filtered_in_order = sorted(drinks_typed, key=lambda drink: drink.num_of_reviews, reverse=order_type)

        elif filter_type == filter_type.RATING:
            drinks_filtered_in_order = sorted(
                drinks_typed, key=lambda drink: float(drink.avg_rating), reverse=order_type
            )

        elif filter_type == filter_type.WISH:
            drinks_filtered_in_order = sorted(drinks_typed, key=lambda drink: drink.num_of_wish, reverse=order_type)

        return drinks_filtered_in_order

    def find_by_drink_id(self, drink_id: DrinkId) -> Optional[Drink]:
        return self.drink_id_to_drink.get(str(drink_id), None)

    def add(self, drink: Drink) -> None:
        self.drink_id_to_drink[str(drink.id)] = drink

    def update(self, drink: Drink) -> None:
        self.drink_id_to_drink[str(drink.id)] = drink

    def delete_by_drink_id(self, drink_id: DrinkId) -> None:
        self.drink_id_to_drink.pop(str(drink_id), None)
