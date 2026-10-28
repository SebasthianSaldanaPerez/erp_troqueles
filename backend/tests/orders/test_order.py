from decimal import Decimal
from uuid import uuid4

import pytest

from src.orders.domain.order import Order, OrderStatus
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money


def test_order_is_created():
    customer_id = uuid4()
    quotation_id = uuid4()

    order = Order(
        customer_id=customer_id,
        origin_quotation_id=quotation_id,
        currency="MXN",
    )

    assert order.id is not None
    assert order.customer_id == customer_id
    assert order.origin_quotation_id == quotation_id
    assert order.status == OrderStatus.CREATED
    assert order.items == ()


def test_order_can_add_item():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    item = OrderItem(
        description="Troquel industrial",
        quantity=2,
        unit_price=Money(
            Decimal("1500.00"),
            "MXN",
        ),
    )

    order.add_item(item)

    assert len(order.items) == 1
    assert order.total.amount == Decimal("3000.00")

def test_order_can_be_started():
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

    order.start()

    assert order.status == OrderStatus.IN_PROGRESS

def test_delivered_order_cannot_be_edited():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    item = OrderItem(
        description="Troquel industrial",
        quantity=1,
        unit_price=Money(Decimal("1000.00"), "MXN"),
    )

    order.add_item(item)
    order.start()
    order.deliver()

    with pytest.raises(ValueError):
        order.update_item(
            item_id=item.id,
            description="Nuevo troquel",
            quantity=2,
            unit_price=Money(Decimal("1500.00"), "MXN"),
        )

def test_order_can_generate_snapshot():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    order.add_item(
        OrderItem(
            description="Troquel industrial",
            quantity=2,
            unit_price=Money(
                Decimal("1000.00"),
                "MXN",
            ),
        )
    )

    snapshot = order.snapshot()

    assert snapshot["status"] == "CREATED"
    assert snapshot["currency"] == "MXN"
    assert len(snapshot["items"]) == 1
    assert snapshot["items"][0]["description"] == "Troquel industrial"
    assert snapshot["total"] == "2000.00"

def test_order_revision_number_starts_at_zero():
    order = Order(
        customer_id=uuid4(),
    )

    assert order.revision_number == 0


def test_order_can_increment_revision():
    order = Order(
        customer_id=uuid4(),
    )

    revision_number = order.increment_revision()

    assert revision_number == 1
    assert order.revision_number == 1