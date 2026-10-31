from decimal import Decimal
from uuid import uuid4

import pytest

from src.orders.application.errors import OrderNotFoundError
from src.orders.application.mark_order_as_paid.command import (
    MarkOrderAsPaidCommand,
)
from src.orders.application.mark_order_as_paid.handler import (
    MarkOrderAsPaidHandler,
)
from src.orders.domain.order import BillingStatus, Order
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_order_repository import InMemoryOrderRepository


def create_order() -> Order:
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    order.add_item(
        OrderItem(
            description="Troquel industrial",
            quantity=1,
            unit_price=Money(
                Decimal("10000.00"),
                "MXN",
            ),
        )
    )

    return order


def test_mark_order_as_paid():
    repository = InMemoryOrderRepository()

    order = create_order()

    order.update_billing_status(
        Money(
            Decimal("10000.00"),
            "MXN",
        )
    )

    repository.save(order)

    handler = MarkOrderAsPaidHandler(repository)

    command = MarkOrderAsPaidCommand(
        order_id=order.id,
    )

    handler.execute(command)

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.billing_status == BillingStatus.PAID


def test_partially_invoiced_order_cannot_be_marked_as_paid():
    repository = InMemoryOrderRepository()

    order = create_order()

    order.update_billing_status(
        Money(
            Decimal("4000.00"),
            "MXN",
        )
    )

    repository.save(order)

    handler = MarkOrderAsPaidHandler(repository)

    command = MarkOrderAsPaidCommand(
        order_id=order.id,
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_not_invoiced_order_cannot_be_marked_as_paid():
    repository = InMemoryOrderRepository()

    order = create_order()
    repository.save(order)

    handler = MarkOrderAsPaidHandler(repository)

    command = MarkOrderAsPaidCommand(
        order_id=order.id,
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_mark_order_as_paid_raises_error_when_order_does_not_exist():
    repository = InMemoryOrderRepository()

    handler = MarkOrderAsPaidHandler(repository)

    command = MarkOrderAsPaidCommand(
        order_id=uuid4(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(command)

