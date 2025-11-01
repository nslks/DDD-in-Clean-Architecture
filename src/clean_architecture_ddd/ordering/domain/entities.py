from __future__ import annotations

from dataclasses import dataclass, field

from clean_architecture_ddd.ordering.domain.value_objects import Money


@dataclass(frozen=True)
class OrderItem:
    product_id: int
    unit_price: Money
    quantity: int = 1

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive.")

    def subtotal(self) -> Money:
        return self.unit_price * self.quantity

    def with_added_quantity(self, additional: int) -> "OrderItem":
        if additional <= 0:
            raise ValueError("Additional quantity must be positive.")
        return OrderItem(
            product_id=self.product_id,
            unit_price=self.unit_price,
            quantity=self.quantity + additional,
        )


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
        for index, existing in enumerate(self.items):
            if existing.product_id == item.product_id:
                self.items[index] = existing.with_added_quantity(item.quantity)
                break
        else:
            self.items.append(item)
