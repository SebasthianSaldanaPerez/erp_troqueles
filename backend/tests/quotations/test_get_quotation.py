from decimal import Decimal
from uuid import uuid4

import pytest

from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.application.get_quotation.handler import (
    GetQuotationHandler,
)
from src.quotations.application.get_quotation.query import GetQuotationQuery
from src.quotations.domain.quotation import Quotation
from src.shared.domain.value_objects.tax_rate import TaxRate
from tests.fakes.in_memory_quotation_repository import (
    InMemoryQuotationRepository,
)


def test_get_quotation():
    repository = InMemoryQuotationRepository()

    quotation = Quotation(
        customer_id=uuid4(),
        tax_rate=TaxRate(Decimal("16")),
    )
    repository.save(quotation)

    handler = GetQuotationHandler(repository)

    result = handler.execute(
        GetQuotationQuery(
            quotation_id=quotation.id,
        )
    )

    assert result.id == quotation.id


def test_get_quotation_raises_error_when_not_found():
    repository = InMemoryQuotationRepository()
    handler = GetQuotationHandler(repository)

    with pytest.raises(QuotationNotFoundError):
        handler.execute(
            GetQuotationQuery(
                quotation_id=uuid4(),
            )
        )