from __future__ import annotations

from clean_architecture.application.create_order import CreateOrderUseCase


class FakeRepo:
    def __init__(self) -> None:
        self.saved_orders = []
        self._next_id = 1

    def next_id(self) -> int:
        current = self._next_id
        self._next_id += 1
        return current

    def save(self, order) -> None:
        self.saved_orders.append(order)


def test_create_order_sums_total_correctly() -> None:
    repo = FakeRepo()
    use_case = CreateOrderUseCase(repo)

    order = use_case.execute(1, [{"price": 10}, {"price": 5}])

    assert order.total == 15
    assert order.user_id == 1
    assert repo.saved_orders[0] is order


def test_create_order_doubles_as_integration() -> None:
    repo = FakeRepo()
    use_case = CreateOrderUseCase(repo)

    order = use_case.execute(2, [{"price": 7.5}, {"price": 2.5}])

    assert len(repo.saved_orders) == 1
    assert order.id == 1
