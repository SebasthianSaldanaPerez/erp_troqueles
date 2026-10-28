from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.accept_quotation.command import (
    AcceptQuotationCommand,
)
from src.quotations.application.accept_quotation.handler import (
    AcceptQuotationHandler,
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


def test_accept_quotation():
    repository = InMemoryQuotationRepository()

    quotation = create_sent_quotation()
    repository.save(quotation)

    handler = AcceptQuotationHandler(repository)

    handler.execute(
        AcceptQuotationCommand(
            quotation_id=quotation.id,
        )
    )

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None
    assert saved_quotation.status == QuotationStatus.ACCEPTED


def test_accept_draft_quotation_raises_error():
    repository = InMemoryQuotationRepository()

    quotation = Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
    )
    repository.save(quotation)

    handler = AcceptQuotationHandler(repository)

    with pytest.raises(ValueError):
        handler.execute(
            AcceptQuotationCommand(
                quotation_id=quotation.id,
            )
        )


def test_accept_quotation_raises_error_when_not_found():
    repository = InMemoryQuotationRepository()
    handler = AcceptQuotationHandler(repository)

    with pytest.raises(QuotationNotFoundError):
        handler.execute(
            AcceptQuotationCommand(
                quotation_id=uuid4(),
            )
        )