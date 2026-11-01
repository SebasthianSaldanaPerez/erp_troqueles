from src.invoices.domain.invoice import Invoice
from src.presentation.api.invoices.schemas import InvoiceResponse


def invoice_to_response(invoice: Invoice) -> InvoiceResponse:
    return InvoiceResponse(
        id=str(invoice.id),
        order_id=str(invoice.order_id),
        folio=invoice.folio,
        invoice_date=invoice.invoice_date,
        total=invoice.total.amount,
        currency=invoice.total.currency,
        status=invoice.status.value,
    )