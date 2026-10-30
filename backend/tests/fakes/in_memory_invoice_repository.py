from src.invoices.domain.invoice import Invoice
from src.invoices.domain.invoice_repository import InvoiceRepository


class InMemoryInvoiceRepository(InvoiceRepository):

    def __init__(self):
        self.invoices = []

    def save(self, invoice: Invoice) -> None:
        for index, existing_invoice in enumerate(self.invoices):
            if existing_invoice.id == invoice.id:
                self.invoices[index] = invoice
                return

        self.invoices.append(invoice)

    def get_by_id(self, invoice_id):
        for invoice in self.invoices:
            if invoice.id == invoice_id:
                return invoice

        return None

    def list_by_order_id(self, order_id):
        return [
            invoice
            for invoice in self.invoices
            if invoice.order_id == order_id
        ]