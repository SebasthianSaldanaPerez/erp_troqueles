from decimal import Decimal

import pytest

from src.shared.domain.value_objects.money import Money


def test_money_is_created():
    money = Money(
        amount=Decimal("1500.00"),
        currency="MXN",
    )

    assert money.amount == Decimal("1500.00")
    assert money.currency == "MXN"


def test_money_normalizes_currency():
    money = Money(
        amount=Decimal("100.00"),
        currency="  mxn  ",
    )

    assert money.currency == "MXN"


def test_money_cannot_be_negative():
    with pytest.raises(ValueError):
        Money(
            amount=Decimal("-1.00"),
            currency="MXN",
        )


def test_money_can_be_added():
    first = Money(Decimal("100.00"), "MXN")
    second = Money(Decimal("50.00"), "MXN")

    result = first.add(second)

    assert result.amount == Decimal("150.00")
    assert result.currency == "MXN"


def test_money_cannot_add_different_currencies():
    mxn = Money(Decimal("100.00"), "MXN")
    usd = Money(Decimal("50.00"), "USD")

    with pytest.raises(ValueError):
        mxn.add(usd)


def test_money_can_be_multiplied():
    money = Money(Decimal("100.00"), "MXN")

    result = money.multiply(3)

    assert result.amount == Decimal("300.00")