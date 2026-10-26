from decimal import Decimal

import pytest

from src.shared.domain.value_objects.tax_rate import TaxRate


def test_tax_rate_is_created():
    tax_rate = TaxRate(Decimal("16"))

    assert tax_rate.value == Decimal("16")


def test_tax_rate_cannot_be_negative():
    with pytest.raises(ValueError):
        TaxRate(Decimal("-1"))


def test_tax_rate_cannot_be_greater_than_100():
    with pytest.raises(ValueError):
        TaxRate(Decimal("101"))


def test_tax_rate_can_be_applied():
    tax_rate = TaxRate(Decimal("16"))

    result = tax_rate.apply_to(Decimal("1000"))

    assert result == Decimal("160")