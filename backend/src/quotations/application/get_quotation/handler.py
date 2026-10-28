from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation import Quotation
from src.quotations.domain.quotation_repository import QuotationRepository

from .query import GetQuotationQuery


class GetQuotationHandler:

    def __init__(self, repository: QuotationRepository):
        self._repository = repository

    def execute(self, query: GetQuotationQuery) -> Quotation:
        quotation = self._repository.get_by_id(query.quotation_id)

        if quotation is None:
            raise QuotationNotFoundError(
                f"Quotation {query.quotation_id} was not found"
            )

        return quotation