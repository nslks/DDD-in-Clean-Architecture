from __future__ import annotations

import pytest

from clean_architecture_ddd.ordering.application.use_cases import CreateOrderUseCase
from clean_architecture_ddd.ordering.infrastructure.order_repository_inmemory import (
    InMemoryOrderRepository,
)
from clean_architecture_ddd.ordering.domain.value_objects import Money
from clean_architecture_ddd.pricing.domain.discount_service import DiscountService


def test_create_order_with_discount_applies_domain_logic() -> None:
    repository = InMemoryOrderRepository()
    discount_service = DiscountService()
    use_case = CreateOrderUseCase(repository, discount_service)

    total = use_case.execute(
        user_id=1,
        items=[
            {"product_id": 1, "price": 10, "quantity": 1},
            {"product_id": 2, "price": 20, "quantity": 1},
        ],
        discount_percentage=10,
    )

    assert total == Money.from_value("27.00")
    saved_order = repository.get(1)
    assert saved_order.total() == Money.from_value("30.00")


def test_create_order_requires_items() -> None:
    repository = InMemoryOrderRepository()
    discount_service = DiscountService()
    use_case = CreateOrderUseCase(repository, discount_service)

    with pytest.raises(ValueError):
        use_case.execute(user_id=1, items=[], discount_percentage=0)
