from __future__ import annotations

import pytest

from clean_architecture_ddd.ordering.domain.value_objects import Money
from clean_architecture_ddd.pricing.domain.discount_service import DiscountService


def test_discount_service_reduces_total_by_percentage() -> None:
    service = DiscountService()
    total = Money.from_value(100)

    discounted = service.apply_discount(total, 10)

    assert discounted == Money.from_value("90.00")


def test_discount_service_rejects_invalid_percentage() -> None:
    service = DiscountService()

    with pytest.raises(ValueError):
        service.apply_discount(Money.from_value(100), 120)
