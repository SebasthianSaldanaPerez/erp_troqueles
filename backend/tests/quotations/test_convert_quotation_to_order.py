from decimal import Decimal
from uuid import uuid4

import pytest

from src.orders.domain.order import OrderStatus
from src.quotations.application.convert_quotation_to_order.command import (
    ConvertQuotationToOrderCommand,
)
from src.quotations.application.convert_quotation_to_order.handler import (
    ConvertQuotationToOrderHandler,
)
from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation import Quotation
from src.quotations.domain.quotation_item import QuotationItem
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate
from tests.fakes.in_memory_order_repository import (
    InMemoryOrderRepository,
)
from tests.fakes.in_memory_quotation_repository import (
    InMemoryQuotationRepository,
)


def create_accepted_quotation() -> Quotation:
    quotation = Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
        currency="MXN",
    )

    quotation.add_item(
        QuotationItem(
            description="Troquel A",
            quantity=2,
            unit_price=Money(
                Decimal("1000.00"),
                "MXN",
            ),
        )
    )

    quotation.send()
    quotation.accept()

    return quotation


def test_convert_quotation_to_order():
    quotation_repository = InMemoryQuotationRepository()
    order_repository = InMemoryOrderRepository()

    quotation = create_accepted_quotation()
    quotation_repository.save(quotation)

    handler = ConvertQuotationToOrderHandler(
        quotation_repository=quotation_repository,
        order_repository=order_repository,
    )

    order_id = handler.execute(
        ConvertQuotationToOrderCommand(
            quotation_id=quotation.id,
        )
    )

    order = order_repository.get_by_id(order_id)

    assert order is not None
    assert order.status == OrderStatus.CREATED
    assert order.customer_id == quotation.customer_id
    assert order.origin_quotation_id == quotation.id
    assert len(order.items) == 1
    assert order.items[0].description == "Troquel A"
    assert order.items[0].quantity == 2
    assert order.total.amount == Decimal("2000.00")


def test_draft_quotation_cannot_be_converted_to_order():
    quotation_repository = InMemoryQuotationRepository()
    order_repository = InMemoryOrderRepository()

    quotation = Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
    )
    quotation_repository.save(quotation)

    handler = ConvertQuotationToOrderHandler(
        quotation_repository,
        order_repository,
    )

    with pytest.raises(ValueError):
        handler.execute(
            ConvertQuotationToOrderCommand(
                quotation_id=quotation.id,
            )
        )


def test_convert_quotation_to_order_raises_error_when_not_found():
    quotation_repository = InMemoryQuotationRepository()
    order_repository = InMemoryOrderRepository()

    handler = ConvertQuotationToOrderHandler(
        quotation_repository,
        order_repository,
    )

    with pytest.raises(QuotationNotFoundError):
        handler.execute(
            ConvertQuotationToOrderCommand(
                quotation_id=uuid4(),
            )
        )