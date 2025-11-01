from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    """Baseline Order entity with minimal behaviour."""

    id: int
    user_id: int
    total: float
    items: list[dict[str, float]]
