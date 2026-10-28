from decimal import Decimal
from uuid import uuid4

from src.quotations.application.list_quotations.handler import (
    ListQuotationsHandler,
)
from src.quotations.application.list_quotations.query import (
    ListQuotationsQuery,
)
from src.quotations.domain.quotation import Quotation
from src.shared.domain.value_objects.tax_rate import TaxRate
from tests.fakes.in_memory_quotation_repository import (
    InMemoryQuotationRepository,
)


def test_list_quotations():
    repository = InMemoryQuotationRepository()

    repository.save(
        Quotation(
            customer_id=uuid4(),
            tax_rate=TaxRate(Decimal("16")),
        )
    )
    repository.save(
        Quotation(
            customer_id=uuid4(),
            tax_rate=TaxRate(Decimal("16")),
        )
    )

    handler = ListQuotationsHandler(repository)

    result = handler.execute(ListQuotationsQuery())

    assert len(result) == 2


def test_list_quotations_returns_empty_list():
    repository = InMemoryQuotationRepository()
    handler = ListQuotationsHandler(repository)

    result = handler.execute(ListQuotationsQuery())

    assert result == []