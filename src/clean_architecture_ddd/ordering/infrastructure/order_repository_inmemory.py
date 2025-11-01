from __future__ import annotations

from typing import Dict, List

from clean_architecture_ddd.ordering.domain.entities import Order
from clean_architecture_ddd.ordering.domain.repositories import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: Dict[int, Order] = {}
        self._next_id: int = 1

    def next_id(self) -> int:
        current = self._next_id
        self._next_id += 1
        return current

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def get(self, order_id: int) -> Order:
        return self._orders[order_id]

    def list_all(self) -> List[Order]:
        return list(self._orders.values())
