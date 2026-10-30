from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.invoices.application.register_invoice.command import (
    RegisterInvoiceCommand,
)
from src.invoices.application.register_invoice.handler import (
    RegisterInvoiceHandler,
)
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order import Order
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_invoice_repository import (
    InMemoryInvoiceRepository,
)
from tests.fakes.in_memory_order_repository import (
    InMemoryOrderRepository,
)


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


def test_register_invoice():
    invoice_repository = InMemoryInvoiceRepository()
    order_repository = InMemoryOrderRepository()

    order = create_order()
    order_repository.save(order)

    handler = RegisterInvoiceHandler(
        invoice_repository=invoice_repository,
        order_repository=order_repository,
    )

    invoice_id = handler.execute(
        RegisterInvoiceCommand(
            order_id=order.id,
            folio="FAC-001",
            invoice_date=date.today(),
            total=Decimal("4000.00"),
            currency="MXN",
        )
    )

    invoice = invoice_repository.get_by_id(invoice_id)

    assert invoice is not None
    assert invoice.folio == "FAC-001"
    assert invoice.total.amount == Decimal("4000.00")


def test_order_can_have_multiple_invoices():
    invoice_repository = InMemoryInvoiceRepository()
    order_repository = InMemoryOrderRepository()

    order = create_order()
    order_repository.save(order)

    handler = RegisterInvoiceHandler(
        invoice_repository,
        order_repository,
    )

    handler.execute(
        RegisterInvoiceCommand(
            order_id=order.id,
            folio="FAC-001",
            invoice_date=date.today(),
            total=Decimal("4000.00"),
        )
    )

    handler.execute(
        RegisterInvoiceCommand(
            order_id=order.id,
            folio="FAC-002",
            invoice_date=date.today(),
            total=Decimal("6000.00"),
        )
    )

    invoices = invoice_repository.list_by_order_id(order.id)

    assert len(invoices) == 2


def test_invoice_cannot_exceed_order_total():
    invoice_repository = InMemoryInvoiceRepository()
    order_repository = InMemoryOrderRepository()

    order = create_order()
    order_repository.save(order)

    handler = RegisterInvoiceHandler(
        invoice_repository,
        order_repository,
    )

    handler.execute(
        RegisterInvoiceCommand(
            order_id=order.id,
            folio="FAC-001",
            invoice_date=date.today(),
            total=Decimal("8000.00"),
        )
    )

    with pytest.raises(ValueError):
        handler.execute(
            RegisterInvoiceCommand(
                order_id=order.id,
                folio="FAC-002",
                invoice_date=date.today(),
                total=Decimal("3000.00"),
            )
        )


def test_register_invoice_raises_error_when_order_does_not_exist():
    handler = RegisterInvoiceHandler(
        InMemoryInvoiceRepository(),
        InMemoryOrderRepository(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(
            RegisterInvoiceCommand(
                order_id=uuid4(),
                folio="FAC-001",
                invoice_date=date.today(),
                total=Decimal("1000.00"),
            )
        )