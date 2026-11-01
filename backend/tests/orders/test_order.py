from decimal import Decimal
from uuid import uuid4

import pytest

from src.shared.domain.value_objects.tax_rate import TaxRate
from src.orders.domain.order import BillingStatus, Order, OrderStatus
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money


def test_order_is_created():
    customer_id = uuid4()
    quotation_id = uuid4()

    order = Order(
        customer_id=customer_id,
        origin_quotation_id=quotation_id,
        tax_rate=TaxRate(Decimal("16")),
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
        tax_rate=TaxRate(Decimal("16")),
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
    assert order.total.amount == Decimal("3480.00")

def test_order_can_be_started():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
        tax_rate=TaxRate(Decimal("16")),
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
        tax_rate=TaxRate(Decimal("16")),
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
        tax_rate=TaxRate(Decimal("16")),
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
    assert snapshot["total"] == "2320.00"

def test_order_revision_number_starts_at_zero():
    order = Order(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
    )

    assert order.revision_number == 0


def test_order_can_increment_revision():
    order = Order(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16"))
    )

    revision_number = order.increment_revision()

    assert revision_number == 1
    assert order.revision_number == 1

def test_order_billing_status_starts_as_not_invoiced():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
        tax_rate=TaxRate(Decimal("0")),
    )

    assert order.billing_status == BillingStatus.NOT_INVOICED

def test_order_can_be_partially_invoiced():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
        tax_rate=TaxRate(Decimal("16")),
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

    order.update_billing_status(
        Money(
            Decimal("4000.00"),
            "MXN",
        )
    )

    assert order.billing_status == BillingStatus.PARTIALLY_INVOICED

def test_order_can_be_fully_invoiced():
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
        tax_rate=TaxRate(Decimal("16"))
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

    order.update_billing_status(
        Money(
            Decimal("11600.00"),
            "MXN",
        )
    )

    assert order.billing_status == BillingStatus.FULLY_INVOICED

def test_order_can_be_rehydrated():
    customer_id = uuid4()
    order_id = uuid4()

    item = OrderItem(
        description="Troquel",
        quantity=1,
        unit_price=Money(
            Decimal("1000.00"),
            "MXN",
        ),
    )

    order = Order.rehydrate(
        order_id=order_id,
        customer_id=customer_id,
        origin_quotation_id=None,
        currency="MXN",
        tax_rate=TaxRate(Decimal("16")),
        status=OrderStatus.DELIVERED,
        billing_status=BillingStatus.FULLY_INVOICED,
        revision_number=3,
        items=[item],
    )

    assert order.id == order_id
    assert order.status == OrderStatus.DELIVERED
    assert order.billing_status == BillingStatus.FULLY_INVOICED
    assert order.revision_number == 3
    assert len(order.items) == 1