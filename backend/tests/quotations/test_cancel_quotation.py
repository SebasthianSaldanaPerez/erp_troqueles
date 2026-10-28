from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.cancel_quotation.command import (
    CancelQuotationCommand,
)
from src.quotations.application.cancel_quotation.handler import (
    CancelQuotationHandler,
)
from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation import Quotation, QuotationStatus
from src.quotations.domain.quotation_item import QuotationItem
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate
from tests.fakes.in_memory_quotation_repository import (
    InMemoryQuotationRepository,
)


def create_sent_quotation() -> Quotation:
    quotation = Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
        currency="MXN",
    )

    quotation.add_item(
        QuotationItem(
            description="Troquel industrial",
            quantity=1,
            unit_price=Money(Decimal("1000.00"), "MXN"),
        )
    )

    quotation.send()

    return quotation

def create_quotation() -> Quotation:
    quotation = Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
        currency="MXN",
    )

    quotation.add_item(
        QuotationItem(
            description="Troquel industrial",
            quantity=1,
            unit_price=Money(Decimal("1000.00"), "MXN"),
        )
    )

    return quotation

def test_cancel_quotation():
    repository = InMemoryQuotationRepository()

    quotation = create_sent_quotation()
    repository.save(quotation)

    handler = CancelQuotationHandler(repository)

    handler.execute(
        CancelQuotationCommand(
            quotation_id=quotation.id,
        )
    )

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None
    assert saved_quotation.status == QuotationStatus.CANCELLED


def test_cancel_quotation_when_is_draft():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    repository.save(quotation)

    handler = CancelQuotationHandler(repository)

    handler.execute(
        CancelQuotationCommand(
            quotation_id=quotation.id,
        )
    )

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None
    assert saved_quotation.status == QuotationStatus.CANCELLED


def test_cancel_quotation_raises_error_when_is_accepted():
    repository = InMemoryQuotationRepository()

    quotation = create_sent_quotation()
    quotation.accept()
    repository.save(quotation)

    handler = CancelQuotationHandler(repository)

    with pytest.raises(ValueError):
        handler.execute(
            CancelQuotationCommand(
                quotation_id=quotation.id,
            )
        )