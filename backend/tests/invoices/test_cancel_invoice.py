from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.invoices.application.cancel_invoice.command import (
    CancelInvoiceCommand,
)
from src.invoices.application.cancel_invoice.handler import (
    CancelInvoiceHandler,
)
from src.invoices.application.errors import InvoiceNotFoundError
from src.invoices.domain.invoice import (
    Invoice,
    InvoiceStatus,
)
from src.orders.domain.order import (
    BillingStatus,
    Order,
)
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate
from tests.fakes.in_memory_invoice_repository import (
    InMemoryInvoiceRepository,
)
from tests.fakes.in_memory_order_repository import (
    InMemoryOrderRepository,
)
from tests.fakes.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)


def create_order() -> Order:
    order = Order(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("0")),
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


def create_invoice(
    order_id,
    total: str,
) -> Invoice:
    return Invoice(
        order_id=order_id,
        folio="FAC-001",
        invoice_date=date.today(),
        total=Money(
            Decimal(total),
            "MXN",
        ),
    )


def test_cancel_invoice():
    invoice_repository = InMemoryInvoiceRepository()
    order_repository = InMemoryOrderRepository()
    unit_of_work = InMemoryUnitOfWork()

    order = create_order()

    order.update_billing_status(
        Money(
            Decimal("4000.00"),
            "MXN",
        )
    )

    order_repository.save(order)

    invoice = create_invoice(
        order_id=order.id,
        total="4000.00",
    )

    invoice_repository.save(invoice)

    handler = CancelInvoiceHandler(
        invoice_repository=invoice_repository,
        order_repository=order_repository,
        unit_of_work=unit_of_work,
    )

    handler.execute(
        CancelInvoiceCommand(
            invoice_id=invoice.id,
        )
    )

    saved_invoice = invoice_repository.get_by_id(
        invoice.id
    )

    saved_order = order_repository.get_by_id(
        order.id
    )

    assert saved_invoice is not None
    assert saved_invoice.status == InvoiceStatus.CANCELLED

    assert saved_order is not None
    assert (
        saved_order.billing_status
        == BillingStatus.NOT_INVOICED
    )

    assert unit_of_work.committed is True

def test_cancelling_invoice_recalculates_order_to_partially_invoiced():
    invoice_repository = InMemoryInvoiceRepository()
    order_repository = InMemoryOrderRepository()
    unit_of_work = InMemoryUnitOfWork()

    order = create_order()

    order.update_billing_status(
        Money(
            Decimal("10000.00"),
            "MXN",
        )
    )

    order_repository.save(order)

    first_invoice = Invoice(
        order_id=order.id,
        folio="FAC-001",
        invoice_date=date.today(),
        total=Money(
            Decimal("4000.00"),
            "MXN",
        ),
    )

    second_invoice = Invoice(
        order_id=order.id,
        folio="FAC-002",
        invoice_date=date.today(),
        total=Money(
            Decimal("6000.00"),
            "MXN",
        ),
    )

    invoice_repository.save(first_invoice)
    invoice_repository.save(second_invoice)

    handler = CancelInvoiceHandler(
        invoice_repository=invoice_repository,
        order_repository=order_repository,
        unit_of_work=unit_of_work,
    )

    handler.execute(
        CancelInvoiceCommand(
            invoice_id=second_invoice.id,
        )
    )

    saved_order = order_repository.get_by_id(
        order.id
    )

    assert saved_order is not None
    assert (
        saved_order.billing_status
        == BillingStatus.PARTIALLY_INVOICED
    )

def test_invoice_from_paid_order_cannot_be_cancelled():
    invoice_repository = InMemoryInvoiceRepository()
    order_repository = InMemoryOrderRepository()
    unit_of_work = InMemoryUnitOfWork()

    order = create_order()

    order.update_billing_status(
        Money(
            Decimal("10000.00"),
            "MXN",
        )
    )

    order.mark_as_paid()

    order_repository.save(order)

    invoice = create_invoice(
        order_id=order.id,
        total="10000.00",
    )

    invoice_repository.save(invoice)

    handler = CancelInvoiceHandler(
        invoice_repository,
        order_repository,
        unit_of_work,
    )

    with pytest.raises(ValueError):
        handler.execute(
            CancelInvoiceCommand(
                invoice_id=invoice.id,
            )
        )

    saved_invoice = invoice_repository.get_by_id(
        invoice.id
    )

    assert saved_invoice is not None
    assert saved_invoice.status == InvoiceStatus.REGISTERED

def test_cancel_invoice_raises_error_when_invoice_does_not_exist():
    handler = CancelInvoiceHandler(
        invoice_repository=InMemoryInvoiceRepository(),
        order_repository=InMemoryOrderRepository(),
        unit_of_work=InMemoryUnitOfWork(),
    )

    with pytest.raises(InvoiceNotFoundError):
        handler.execute(
            CancelInvoiceCommand(
                invoice_id=uuid4(),
            )
        )