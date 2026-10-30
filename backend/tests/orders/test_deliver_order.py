from decimal import Decimal
from uuid import uuid4

import pytest

from src.orders.application.deliver_order.command import DeliverOrderCommand
from src.orders.application.deliver_order.handler import DeliverOrderHandler
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


def test_deliver_order():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    order.start()
    repository.save(order)

    handler = DeliverOrderHandler(repository)

    command = DeliverOrderCommand(
        order_id=order.id,
    )

    handler.execute(command)

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatus.DELIVERED


def test_created_order_cannot_be_delivered():
    repository = InMemoryOrderRepository()

    order = create_order_with_item()
    repository.save(order)

    handler = DeliverOrderHandler(repository)

    command = DeliverOrderCommand(
        order_id=order.id,
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_deliver_order_raises_error_when_order_does_not_exist():
    repository = InMemoryOrderRepository()

    handler = DeliverOrderHandler(repository)

    command = DeliverOrderCommand(
        order_id=uuid4(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(command)