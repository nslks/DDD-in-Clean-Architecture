from __future__ import annotations

from dataclasses import dataclass, field

from clean_architecture_ddd.ordering.domain.value_objects import Money


@dataclass(frozen=True)
class OrderItem:
    product_id: int
    unit_price: Money
    quantity: int = 1

    def subtotal(self) -> Money:
        return self.unit_price * self.quantity


@dataclass
class Order:
    id: int
    user_id: int
    items: list[OrderItem] = field(default_factory=list)

    def total(self) -> Money:
        total = Money.zero()
        for item in self.items:
            total += item.subtotal()
        return total

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)
