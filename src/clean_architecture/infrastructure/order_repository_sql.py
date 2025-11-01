from __future__ import annotations

from typing import Dict, List

from clean_architecture.domain.entities import Order


class SqlOrderRepository:
    """In-memory stand-in for a SQL repository."""

    def __init__(self) -> None:
        self._orders: Dict[int, Order] = {}
        self._next_id: int = 1

    def next_id(self) -> int:
        current = self._next_id
        self._next_id += 1
        return current

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def list_orders(self) -> List[Order]:
        return list(self._orders.values())

    def get(self, order_id: int) -> Order:
        return self._orders[order_id]
