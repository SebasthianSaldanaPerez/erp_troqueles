from uuid import UUID

from src.quotations.domain.quotation import Quotation
from src.quotations.domain.quotation_repository import QuotationRepository
from src.shared.domain.value_objects.tax_rate import TaxRate

from .command import CreateQuotationCommand


class CreateQuotationHandler:

    def __init__(self, repository: QuotationRepository):
        self._repository = repository

    def execute(self, command: CreateQuotationCommand) -> UUID:
        tax_rate = TaxRate(command.tax_rate)

        quotation = Quotation(
            customer_id=command.customer_id,
            tax_rate=tax_rate,
            currency=command.currency,
        )

        self._repository.save(quotation)

        return quotation.id