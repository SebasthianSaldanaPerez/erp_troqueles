from decimal import Decimal
from uuid import uuid4

import pytest

from src.orders.application.errors import OrderNotFoundError
from src.orders.application.start_order.command import StartOrderCommand
from src.orders.application.start_order.handler import StartOrderHandler
from src.orders.domain.order import Order, OrderStatus
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_order_repository import InMemoryOrderRepository


def create_order_with_item() -> Order:
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    order.add_item(
        OrderItem(
            description="Troquel industrial",
            quantity=1,
            unit_price=Money(Decimal("1000.00"), "MXN"),
        )
    )

    return order


def test_start_order():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    repository.save(order)

    handler = StartOrderHandler(repository)

    handler.execute(
        StartOrderCommand(
            order_id=order.id,
        )
    )

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatus.IN_PROGRESS


def test_start_empty_order_raises_error():
    repository = InMemoryOrderRepository()

    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )
    repository.save(order)

    handler = StartOrderHandler(repository)

    with pytest.raises(ValueError):
        handler.execute(
            StartOrderCommand(
                order_id=order.id,
            )
        )


def test_start_order_raises_error_when_not_found():
    repository = InMemoryOrderRepository()
    handler = StartOrderHandler(repository)

    with pytest.raises(OrderNotFoundError):
        handler.execute(
            StartOrderCommand(
                order_id=uuid4(),
            )
        )