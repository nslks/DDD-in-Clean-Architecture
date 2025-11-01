from __future__ import annotations

from dataclasses import dataclass

from clean_architecture_ddd.ordering.domain.value_objects import Money


@dataclass
class DiscountService:
    """Simple domain service that applies percentage-based discounts."""

    def apply_discount(self, total: Money, percentage: int) -> Money:
        if percentage <= 0:
            return total
        if percentage > 100:
            raise ValueError("Discount cannot exceed 100 percent.")
        discount_amount = total.percent(percentage)
        return total - discount_amount
