from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from clean_architecture.domain.entities import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        ...

    def next_id(self) -> int:
        ...


@dataclass
class CreateOrderUseCase:
    repository: OrderRepository

    def execute(self, user_id: int, items: Iterable[dict[str, float]]) -> Order:
        item_list = list(items)
        total = sum(item["price"] for item in item_list)
        order = Order(id=self.repository.next_id(), user_id=user_id, total=total, items=item_list)
        self.repository.save(order)
        return order
