from decimal import Decimal

import pytest

from src.quotations.domain.quotation_item import QuotationItem
from src.shared.domain.value_objects.money import Money


def test_quotation_item_is_created():
    item = QuotationItem(
        description="Troquel industrial",
        quantity=2,
        unit_price=Money(Decimal("1500.00"), "MXN"),
    )

    assert item.description == "Troquel industrial"
    assert item.quantity == 2
    assert item.unit_price.amount == Decimal("1500.00")
    assert item.id is not None


def test_quotation_item_calculates_total():
    item = QuotationItem(
        description="Troquel industrial",
        quantity=3,
        unit_price=Money(Decimal("1500.00"), "MXN"),
    )

    assert item.total.amount == Decimal("4500.00")
    assert item.total.currency == "MXN"


def test_quotation_item_requires_description():
    with pytest.raises(ValueError):
        QuotationItem(
            description="",
            quantity=1,
            unit_price=Money(Decimal("100.00"), "MXN"),
        )


def test_quotation_item_quantity_must_be_greater_than_zero():
    with pytest.raises(ValueError):
        QuotationItem(
            description="Troquel industrial",
            quantity=0,
            unit_price=Money(Decimal("100.00"), "MXN"),
        )


def test_quotation_item_can_change_quantity():
    item = QuotationItem(
        description="Troquel industrial",
        quantity=1,
        unit_price=Money(Decimal("100.00"), "MXN"),
    )

    item.change_quantity(5)

    assert item.quantity == 5
    assert item.total.amount == Decimal("500.00")


def test_quotation_item_can_change_unit_price():
    item = QuotationItem(
        description="Troquel industrial",
        quantity=2,
        unit_price=Money(Decimal("100.00"), "MXN"),
    )

    item.change_unit_price(
        Money(Decimal("250.00"), "MXN")
    )

    assert item.unit_price.amount == Decimal("250.00")
    assert item.total.amount == Decimal("500.00")