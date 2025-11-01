from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Union


Number = Union[int, float, str, Decimal, "Money"]


def _to_decimal(value: Number) -> Decimal:
    if isinstance(value, Money):
        return value.amount
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self) -> None:
        quantized = self._quantize(self.amount)
        object.__setattr__(self, "amount", quantized)

    @staticmethod
    def _quantize(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @classmethod
    def from_value(cls, value: Number) -> "Money":
        return cls(_to_decimal(value))

    @classmethod
    def zero(cls) -> "Money":
        return cls(Decimal("0"))

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __sub__(self, other: "Money") -> "Money":
        return Money(self.amount - other.amount)

    def __mul__(self, multiplier: Union[int, Decimal, float]) -> "Money":
        decimal_multiplier = _to_decimal(multiplier)
        return Money(self.amount * decimal_multiplier)

    __rmul__ = __mul__

    def percent(self, value: int) -> "Money":
        return Money(self.amount * _to_decimal(value) / Decimal(100))

    def __str__(self) -> str:
        return f"{self.amount:.2f}"
