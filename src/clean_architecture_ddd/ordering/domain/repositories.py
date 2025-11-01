from __future__ import annotations

from typing import Protocol

from clean_architecture_ddd.ordering.domain.entities import Order


class OrderRepository(Protocol):
    def next_id(self) -> int:
        ...

    def save(self, order: Order) -> None:
        ...

    def get(self, order_id: int) -> Order:
        ...

    def list_all(self) -> list[Order]:
        ...
