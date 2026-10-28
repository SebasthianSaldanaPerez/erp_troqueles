from src.quotations.domain.quotation import Quotation
from src.quotations.domain.quotation_repository import QuotationRepository

from .query import ListQuotationsQuery


class ListQuotationsHandler:

    def __init__(self, repository: QuotationRepository):
        self._repository = repository

    def execute(self, query: ListQuotationsQuery) -> list[Quotation]:
        return self._repository.list_all()