from decimal import Decimal
from uuid import uuid4

import pytest

from src.orders.application.cancel_order.command import CancelOrderCommand
from src.orders.application.cancel_order.handler import CancelOrderHandler
from src.orders.application.errors import OrderNotFoundError
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
            unit_price=Money(
                Decimal("1000.00"),
                "MXN",
            ),
        )
    )

    return order


def test_created_order_can_be_cancelled():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    repository.save(order)

    handler = CancelOrderHandler(repository)

    handler.execute(
        CancelOrderCommand(
            order_id=order.id,
        )
    )

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatus.CANCELLED


def test_in_progress_order_can_be_cancelled():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    order.start()
    repository.save(order)

    handler = CancelOrderHandler(repository)

    handler.execute(
        CancelOrderCommand(
            order_id=order.id,
        )
    )

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatus.CANCELLED


def test_delivered_order_cannot_be_cancelled():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    order.start()
    order.deliver()
    repository.save(order)

    handler = CancelOrderHandler(repository)

    with pytest.raises(ValueError):
        handler.execute(
            CancelOrderCommand(
                order_id=order.id,
            )
        )


def test_cancelled_order_cannot_be_cancelled_again():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    order.cancel()
    repository.save(order)

    handler = CancelOrderHandler(repository)

    with pytest.raises(ValueError):
        handler.execute(
            CancelOrderCommand(
                order_id=order.id,
            )
        )


def test_cancel_order_raises_error_when_order_does_not_exist():
    repository = InMemoryOrderRepository()

    handler = CancelOrderHandler(repository)

    with pytest.raises(OrderNotFoundError):
        handler.execute(
            CancelOrderCommand(
                order_id=uuid4(),
            )
        )