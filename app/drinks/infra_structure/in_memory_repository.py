from typing import List, Optional

from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository, QueryParam
from drinks.domain.value_objects import FilterType, OrderType
from shared_kernel.domain.value_objects import DrinkId


class InMemoryDrinkRepository(DrinkRepository):
    def __init__(self) -> None:
        self.drink_id_to_drink = {}

    # only for test purpose
    def find_all_simple(self) -> List[Drink]:
        return list(self.drink_id_to_drink.values())

    def find_all(self, query_param: QueryParam) -> List[Drink]:
        drinks = list(self.drink_id_to_drink.values())
        drinks_typed = [drink for drink in drinks if drink.type == query_param.drink]

        drinks_filtered_in_order = []
        filter_type = FilterType.from_str(query_param.filter)
        is_order_type = query_param.order != OrderType.DESC
        if filter_type == FilterType.REVIEW:
            drinks_filtered_in_order = sorted(
                drinks_typed,
                key=lambda drink: drink.num_of_reviews,
                reverse=is_order_type,
            )
        elif filter_type == FilterType.RATING:
            drinks_filtered_in_order = sorted(
                drinks_typed,
                key=lambda drink: float(drink.avg_rating),
                reverse=is_order_type,
            )
        elif filter_type == FilterType.WISH:
            drinks_filtered_in_order = sorted(
                drinks_typed, key=lambda drink: drink.num_of_wish, reverse=is_order_type
            )

        return drinks_filtered_in_order

    def find_by_drink_id(self, drink_id: DrinkId) -> Optional[Drink]:
        return self.drink_id_to_drink.get(str(drink_id), None)

    def add(self, drink: Drink) -> None:
        self.drink_id_to_drink[str(drink.id)] = drink

    def update(self, drink: Drink) -> None:
        self.drink_id_to_drink[str(drink.id)] = drink

    def delete_by_drink_id(self, drink_id: DrinkId) -> None:
        self.drink_id_to_drink.pop(str(drink_id), None)
