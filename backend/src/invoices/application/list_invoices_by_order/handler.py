from src.invoices.domain.invoice import Invoice
from src.invoices.domain.invoice_repository import InvoiceRepository

from .query import ListInvoicesByOrderQuery


class ListInvoicesByOrderHandler:

    def __init__(self, repository: InvoiceRepository):
        self._repository = repository

    def execute(
        self,
        query: ListInvoicesByOrderQuery,
    ) -> list[Invoice]:
        return self._repository.list_by_order_id(
            query.order_id
        )