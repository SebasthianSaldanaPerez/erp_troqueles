from decimal import Decimal
from uuid import uuid4

from src.quotations.application.create_quotation.command import (
    CreateQuotationCommand,
)
from src.quotations.application.create_quotation.handler import (
    CreateQuotationHandler,
)
from src.quotations.domain.quotation import QuotationStatus
from tests.fakes.in_memory_quotation_repository import (
    InMemoryQuotationRepository,
)


def test_create_quotation():
    repository = InMemoryQuotationRepository()
    handler = CreateQuotationHandler(repository)

    customer_id = uuid4()

    command = CreateQuotationCommand(
        customer_id=customer_id,
        tax_rate=Decimal("16"),
        currency="MXN",
    )

    quotation_id = handler.execute(command)

    saved_quotation = repository.get_by_id(quotation_id)

    assert quotation_id is not None
    assert saved_quotation is not None
    assert saved_quotation.customer_id == customer_id
    assert saved_quotation.status == QuotationStatus.DRAFT
    assert saved_quotation.items == ()