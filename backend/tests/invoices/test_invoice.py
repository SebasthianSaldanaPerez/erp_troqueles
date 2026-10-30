from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.invoices.domain.invoice import Invoice, InvoiceStatus
from src.shared.domain.value_objects.money import Money


def test_invoice_is_created():
    invoice = Invoice(
        order_id=uuid4(),
        folio="FAC-001",
        invoice_date=date.today(),
        total=Money(Decimal("5000.00"), "MXN"),
    )

    assert invoice.id is not None
    assert invoice.folio == "FAC-001"
    assert invoice.total.amount == Decimal("5000.00")
    assert invoice.status == InvoiceStatus.REGISTERED


def test_invoice_requires_folio():
    with pytest.raises(ValueError):
        Invoice(
            order_id=uuid4(),
            folio="",
            invoice_date=date.today(),
            total=Money(Decimal("5000.00"), "MXN"),
        )


def test_invoice_can_be_cancelled():
    invoice = Invoice(
        order_id=uuid4(),
        folio="FAC-001",
        invoice_date=date.today(),
        total=Money(Decimal("5000.00"), "MXN"),
    )

    invoice.cancel()

    assert invoice.status == InvoiceStatus.CANCELLED


def test_cancelled_invoice_cannot_be_cancelled_again():
    invoice = Invoice(
        order_id=uuid4(),
        folio="FAC-001",
        invoice_date=date.today(),
        total=Money(Decimal("5000.00"), "MXN"),
    )

    invoice.cancel()

    with pytest.raises(ValueError):
        invoice.cancel()