from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from clean_architecture_ddd.ordering.domain.entities import Order, OrderItem
from clean_architecture_ddd.ordering.domain.repositories import OrderRepository
from clean_architecture_ddd.ordering.domain.value_objects import Money
from clean_architecture_ddd.pricing.domain.discount_service import DiscountService


@dataclass(frozen=True)
class OrderItemDTO:
    product_id: int
    price: Money
    quantity: int = 1

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "OrderItemDTO":
        price_value = data.get("price")
        if price_value is None:
            raise ValueError("Order item requires a price.")
        product_id_value = data.get("product_id")
        if product_id_value is None:
            raise ValueError("Order item requires a product_id.")
        quantity_value = data.get("quantity", 1)
        return cls(
            product_id=int(product_id_value),
            price=Money.from_value(price_value),
            quantity=int(quantity_value),
        )

    def to_domain(self) -> OrderItem:
        return OrderItem(
            product_id=self.product_id,
            unit_price=self.price,
            quantity=self.quantity,
        )


@dataclass
class CreateOrderUseCase:
    order_repository: OrderRepository
    discount_service: DiscountService

    def execute(
        self,
        user_id: int,
        items: Iterable[Mapping[str, object]],
        discount_percentage: int = 0,
    ) -> Money:
        item_dtos = [OrderItemDTO.from_mapping(item) for item in items]
        if not item_dtos:
            raise ValueError("Order requires at least one item.")

        order = Order(id=self.order_repository.next_id(), user_id=user_id)
        for dto in item_dtos:
            order.add_item(dto.to_domain())
        self.order_repository.save(order)

        total = order.total()
        return self.discount_service.apply_discount(total, discount_percentage)
