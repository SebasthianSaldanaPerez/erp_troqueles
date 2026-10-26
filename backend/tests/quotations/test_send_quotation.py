from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.application.send_quotation.command import (
    SendQuotationCommand,
)
from src.quotations.application.send_quotation.handler import (
    SendQuotationHandler,
)
from src.quotations.domain.quotation import Quotation, QuotationStatus
from src.quotations.domain.quotation_item import QuotationItem
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate
from tests.fakes.in_memory_quotation_repository import (
    InMemoryQuotationRepository,
)


def create_quotation() -> Quotation:
    return Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
        currency="MXN",
    )


def create_item() -> QuotationItem:
    return QuotationItem(
        description="Troquel industrial",
        quantity=1,
        unit_price=Money(
            Decimal("1000.00"),
            "MXN",
        ),
    )


def test_send_quotation():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    quotation.add_item(create_item())
    repository.save(quotation)

    handler = SendQuotationHandler(repository)

    command = SendQuotationCommand(
        quotation_id=quotation.id,
    )

    handler.execute(command)

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None
    assert saved_quotation.status == QuotationStatus.SENT


def test_send_empty_quotation_raises_error():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    repository.save(quotation)

    handler = SendQuotationHandler(repository)

    command = SendQuotationCommand(
        quotation_id=quotation.id,
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_send_quotation_raises_error_when_quotation_does_not_exist():
    repository = InMemoryQuotationRepository()

    handler = SendQuotationHandler(repository)

    command = SendQuotationCommand(
        quotation_id=uuid4(),
    )

    with pytest.raises(QuotationNotFoundError):
        handler.execute(command)