from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.application.update_quotation_item.command import (
    UpdateQuotationItemCommand,
)
from src.quotations.application.update_quotation_item.handler import (
    UpdateQuotationItemHandler,
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
        description="Troquel inicial",
        quantity=1,
        unit_price=Money(
            Decimal("1000.00"),
            "MXN",
        ),
    )


def test_update_quotation_item():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    item = create_item()
    quotation.add_item(item)

    repository.save(quotation)

    handler = UpdateQuotationItemHandler(repository)

    command = UpdateQuotationItemCommand(
        quotation_id=quotation.id,
        item_id=item.id,
        description="Troquel actualizado",
        quantity=2,
        unit_price=Decimal("1500.00"),
        currency="MXN",
    )

    handler.execute(command)

    saved_quotation = repository.get_by_id(quotation.id)

    assert saved_quotation is not None

    updated_item = saved_quotation.items[0]

    assert updated_item.description == "Troquel actualizado"
    assert updated_item.quantity == 2
    assert updated_item.unit_price.amount == Decimal("1500.00")
    assert updated_item.total.amount == Decimal("3000.00")


def test_update_quotation_item_updates_quotation_totals():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    item = create_item()
    quotation.add_item(item)

    repository.save(quotation)

    handler = UpdateQuotationItemHandler(repository)

    command = UpdateQuotationItemCommand(
        quotation_id=quotation.id,
        item_id=item.id,
        description="Troquel actualizado",
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


def test_update_quotation_item_raises_error_when_quotation_does_not_exist():
    repository = InMemoryQuotationRepository()

    handler = UpdateQuotationItemHandler(repository)

    command = UpdateQuotationItemCommand(
        quotation_id=uuid4(),
        item_id=uuid4(),
        description="Troquel",
        quantity=1,
        unit_price=Decimal("1000.00"),
        currency="MXN",
    )

    with pytest.raises(QuotationNotFoundError):
        handler.execute(command)


def test_update_quotation_item_raises_error_when_item_does_not_exist():
    repository = InMemoryQuotationRepository()

    quotation = create_quotation()
    repository.save(quotation)

    handler = UpdateQuotationItemHandler(repository)

    command = UpdateQuotationItemCommand(
        quotation_id=quotation.id,
        item_id=uuid4(),
        description="Troquel",
        quantity=1,
        unit_price=Decimal("1000.00"),
        currency="MXN",
    )

    with pytest.raises(ValueError):
        handler.execute(command)