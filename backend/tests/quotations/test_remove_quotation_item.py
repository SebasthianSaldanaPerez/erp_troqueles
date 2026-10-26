from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.application.remove_quotation_item.command import (
    RemoveQuotationItemCommand,
)
from src.quotations.application.remove_quotation_item.handler import (
    RemoveQuotationItemHandler,
)
from src.quotations.domain.quotation import Quotation
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
        quantity=2,
        unit_price=Money(
            Decimal("1000.00"),
            "MXN",
        ),
    )


def test_remove_quotation_item():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    item = create_item()
    quotation.add_item(item)

    repository.save(quotation)

    handler = RemoveQuotationItemHandler(repository)

    command = RemoveQuotationItemCommand(
        quotation_id=quotation.id,
        item_id=item.id,
    )

    handler.execute(command)

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None
    assert saved_quotation.items == ()
    assert saved_quotation.subtotal.amount == Decimal("0")
    assert saved_quotation.total.amount == Decimal("0")


def test_remove_quotation_item_raises_error_when_quotation_does_not_exist():
    repository = InMemoryQuotationRepository()
    handler = RemoveQuotationItemHandler(repository)

    command = RemoveQuotationItemCommand(
        quotation_id=uuid4(),
        item_id=uuid4(),
    )

    with pytest.raises(QuotationNotFoundError):
        handler.execute(command)


def test_remove_quotation_item_raises_error_when_item_does_not_exist():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    repository.save(quotation)

    handler = RemoveQuotationItemHandler(repository)

    command = RemoveQuotationItemCommand(
        quotation_id=quotation.id,
        item_id=uuid4(),
    )

    with pytest.raises(ValueError):
        handler.execute(command)