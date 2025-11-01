from __future__ import annotations

import pytest

from clean_architecture_ddd.ordering.domain.entities import Order, OrderItem
from clean_architecture_ddd.ordering.domain.value_objects import Money


def test_order_total_aggregates_item_subtotals() -> None:
    items = [
        OrderItem(product_id=1, unit_price=Money.from_value("10.00"), quantity=1),
        OrderItem(product_id=2, unit_price=Money.from_value("5.00"), quantity=2),
    ]
    order = Order(id=1, user_id=10, items=items)

    assert order.total() == Money.from_value("20.00")


def test_add_item_mutates_order_without_affecting_value_object() -> None:
    order = Order(id=1, user_id=10)
    new_item = OrderItem(product_id=3, unit_price=Money.from_value(2.5), quantity=4)

    order.add_item(new_item)

    assert order.items[-1].subtotal() == Money.from_value("10.00")
    assert order.total() == Money.from_value("10.00")


def test_add_item_merges_existing_product_quantities() -> None:
    base_item = OrderItem(product_id=1, unit_price=Money.from_value(5), quantity=2)
    order = Order(id=1, user_id=10, items=[base_item])

    order.add_item(OrderItem(product_id=1, unit_price=Money.from_value(5), quantity=3))

    assert len(order.items) == 1
    assert order.items[0].quantity == 5
    assert order.total() == Money.from_value("25.00")


def test_invalid_quantity_raises_error() -> None:
    with pytest.raises(ValueError):
        OrderItem(product_id=1, unit_price=Money.from_value(5), quantity=0)
