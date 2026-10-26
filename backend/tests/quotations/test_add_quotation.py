from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.add_quotation_item.command import (
    AddQuotationItemCommand,
)
from src.quotations.application.add_quotation_item.handler import (
    AddQuotationItemHandler,
)
from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation import Quotation
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


def test_add_quotation_item():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    repository.save(quotation)

    handler = AddQuotationItemHandler(repository)

    command = AddQuotationItemCommand(
        quotation_id=quotation.id,
        description="Troquel industrial",
        quantity=2,
        unit_price=Decimal("1500.00"),
        currency="MXN",
    )

    item_id = handler.execute(command)

    saved_quotation = repository.get_by_id(quotation.id)

    assert item_id is not None
    assert saved_quotation is not None
    assert len(saved_quotation.items) == 1
    assert saved_quotation.items[0].description == "Troquel industrial"
    assert saved_quotation.items[0].quantity == 2
    assert saved_quotation.items[0].unit_price.amount == Decimal("1500.00")


def test_add_quotation_item_updates_totals():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    repository.save(quotation)

    handler = AddQuotationItemHandler(repository)

    command = AddQuotationItemCommand(
        quotation_id=quotation.id,
        description="Troquel industrial",
        quantity=2,
        unit_price=Decimal("1000.00"),
        currency="MXN",
    )

    handler.execute(command)

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None
    assert saved_quotation.subtotal.amount == Decimal("2000.00")
    assert saved_quotation.tax.amount == Decimal("320.00")
    assert saved_quotation.total.amount == Decimal("2320.00")


def test_add_quotation_item_raises_error_when_quotation_does_not_exist():
    repository = InMemoryQuotationRepository()
    handler = AddQuotationItemHandler(repository)

    command = AddQuotationItemCommand(
        quotation_id=uuid4(),
        description="Troquel industrial",
        quantity=1,
        unit_price=Decimal("1000.00"),
        currency="MXN",
    )

    with pytest.raises(QuotationNotFoundError):
        handler.execute(command)