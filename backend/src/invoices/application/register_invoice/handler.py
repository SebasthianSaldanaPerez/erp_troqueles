from uuid import UUID
from decimal import Decimal
from src.invoices.domain.invoice import Invoice, InvoiceStatus
from src.invoices.domain.invoice_repository import InvoiceRepository
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository
from src.shared.domain.value_objects.money import Money

from .command import RegisterInvoiceCommand


class RegisterInvoiceHandler:

    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        order_repository: OrderRepository,
    ):
        self._invoice_repository = invoice_repository
        self._order_repository = order_repository

    def execute(self, command: RegisterInvoiceCommand) -> UUID:
        order = self._order_repository.get_by_id(command.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {command.order_id} was not found"
            )

        existing_invoices = self._invoice_repository.list_by_order_id(
            command.order_id
        )

        invoiced_amount = sum(
            (
                invoice.total.amount
                for invoice in existing_invoices
                if invoice.status == InvoiceStatus.REGISTERED
            ),
            Decimal("0"),
        )

        new_total = invoiced_amount + command.total

        if new_total > order.total.amount:
            raise ValueError("Invoice total exceeds remaining order amount")

        invoice = Invoice(
            order_id=command.order_id,
            folio=command.folio,
            invoice_date=command.invoice_date,
            total=Money(
                amount=command.total,
                currency=command.currency,
            ),
        )

        self._invoice_repository.save(invoice)

        return invoice.id