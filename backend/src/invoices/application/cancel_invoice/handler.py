from decimal import Decimal

from src.invoices.application.errors import InvoiceNotFoundError
from src.invoices.domain.invoice import InvoiceStatus
from src.invoices.domain.invoice_repository import InvoiceRepository
from src.orders.domain.order import BillingStatus
from src.orders.domain.order_repository import OrderRepository
from src.shared.application.unit_of_work import UnitOfWork
from src.shared.domain.value_objects.money import Money

from .command import CancelInvoiceCommand


class CancelInvoiceHandler:

    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        order_repository: OrderRepository,
        unit_of_work: UnitOfWork,
    ):
        self._invoice_repository = invoice_repository
        self._order_repository = order_repository
        self._unit_of_work = unit_of_work

    def execute(self, command: CancelInvoiceCommand) -> None:
        with self._unit_of_work:
            invoice = self._invoice_repository.get_by_id(
                command.invoice_id
            )

            if invoice is None:
                raise InvoiceNotFoundError(
                    f"Invoice {command.invoice_id} was not found"
                )

            order = self._order_repository.get_by_id(
                invoice.order_id
            )

            if order is None:
                raise ValueError(
                    "Order associated with invoice was not found"
                )

            if order.billing_status == BillingStatus.PAID:
                raise ValueError(
                    "Invoices from paid orders cannot be cancelled"
                )

            invoice.cancel()

            # IMPORTANTE:
            # primero actualizamos la invoice dentro de la sesión
            self._invoice_repository.save(invoice)

            invoices = self._invoice_repository.list_by_order_id(
                order.id
            )

            invoiced_amount = sum(
                (
                    existing_invoice.total.amount
                    for existing_invoice in invoices
                    if existing_invoice.status
                    == InvoiceStatus.REGISTERED
                ),
                Decimal("0"),
            )

            order.update_billing_status(
                Money(
                    amount=invoiced_amount,
                    currency=order.currency,
                )
            )

            self._order_repository.save(order)

            self._unit_of_work.commit()