from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.domain.quotation import Quotation, QuotationStatus
from src.quotations.domain.quotation_item import QuotationItem
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate


def create_quotation() -> Quotation:
    return Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
        currency="MXN",
    )


def create_item(
    quantity: int = 1,
    price: str = "100.00",
) -> QuotationItem:
    return QuotationItem(
        description="Troquel industrial",
        quantity=quantity,
        unit_price=Money(
            Decimal(price),
            "MXN",
        ),
    )


def test_quotation_is_created_as_draft():
    quotation = create_quotation()

    assert quotation.status == QuotationStatus.DRAFT
    assert quotation.items == ()


def test_quotation_can_add_item():
    quotation = create_quotation()

    quotation.add_item(create_item())

    assert len(quotation.items) == 1


def test_quotation_calculates_subtotal():
    quotation = create_quotation()

    quotation.add_item(
        create_item(quantity=2, price="100.00")
    )

    quotation.add_item(
        create_item(quantity=1, price="50.00")
    )

    assert quotation.subtotal.amount == Decimal("250.00")


def test_quotation_calculates_tax():
    quotation = create_quotation()

    quotation.add_item(
        create_item(quantity=1, price="1000.00")
    )

    assert quotation.tax.amount == Decimal("160.00")


def test_quotation_calculates_total():
    quotation = create_quotation()

    quotation.add_item(
        create_item(quantity=1, price="1000.00")
    )

    assert quotation.total.amount == Decimal("1160.00")


def test_quotation_can_be_sent():
    quotation = create_quotation()
    quotation.add_item(create_item())

    quotation.send()

    assert quotation.status == QuotationStatus.SENT


def test_empty_quotation_cannot_be_sent():
    quotation = create_quotation()

    with pytest.raises(ValueError):
        quotation.send()


def test_sent_quotation_can_be_accepted():
    quotation = create_quotation()
    quotation.add_item(create_item())
    quotation.send()

    quotation.accept()

    assert quotation.status == QuotationStatus.ACCEPTED


def test_draft_quotation_cannot_be_accepted():
    quotation = create_quotation()

    with pytest.raises(ValueError):
        quotation.accept()


def test_sent_quotation_can_be_rejected():
    quotation = create_quotation()
    quotation.add_item(create_item())
    quotation.send()

    quotation.reject()

    assert quotation.status == QuotationStatus.REJECTED


def test_sent_quotation_cannot_be_edited():
    quotation = create_quotation()
    quotation.add_item(create_item())
    quotation.send()

    with pytest.raises(ValueError):
        quotation.add_item(create_item())