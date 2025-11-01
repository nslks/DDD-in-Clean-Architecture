from __future__ import annotations

import argparse
import json
from typing import Any, Iterable, List, Mapping

from clean_architecture_ddd.ordering.application.use_cases import CreateOrderUseCase
from clean_architecture_ddd.ordering.infrastructure.order_repository_inmemory import (
    InMemoryOrderRepository,
)
from clean_architecture_ddd.pricing.domain.discount_service import DiscountService


def parse_items(raw: str) -> List[Mapping[str, Any]]:
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("Items müssen als Liste vorliegen.")
    return [dict(item) for item in data]


def ensure_product_ids(items: Iterable[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    enriched: List[Mapping[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        if "price" not in item:
            raise ValueError("Jedes Item benötigt einen 'price'-Schlüssel.")
        if "product_id" not in item:
            item = dict(item)
            item["product_id"] = idx
        enriched.append(item)
    return enriched


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Berechnet den Bestellwert über die DDD-Variante des Projekts."
    )
    parser.add_argument("--user", type=int, required=True, help="Benutzer-ID")
    parser.add_argument("--items", type=str, required=True, help="JSON-Liste der Items")
    parser.add_argument(
        "--discount",
        type=int,
        default=0,
        help="Rabatt in Prozent, der auf den Gesamtpreis angewendet wird.",
    )
    args = parser.parse_args()

    raw_items = parse_items(args.items)
    items = ensure_product_ids(raw_items)

    use_case = CreateOrderUseCase(InMemoryOrderRepository(), DiscountService())
    total = use_case.execute(args.user, items, args.discount)

    print(f"Gesamtsumme nach Rabatt: {total}")


if __name__ == "__main__":
    main()
