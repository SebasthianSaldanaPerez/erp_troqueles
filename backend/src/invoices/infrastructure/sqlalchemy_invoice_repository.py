from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.invoice_model import InvoiceModel
from src.invoices.domain.invoice import Invoice, InvoiceStatus
from src.invoices.domain.invoice_repository import InvoiceRepository
from src.shared.domain.value_objects.money import Money


class SQLAlchemyInvoiceRepository(InvoiceRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, invoice: Invoice) -> None:
        model = self._session.get(
            InvoiceModel,
            invoice.id,
        )

        if model is None:
            model = InvoiceModel(
                id=invoice.id,
                order_id=invoice.order_id,
                folio=invoice.folio,
                invoice_date=invoice.invoice_date,
                total=invoice.total.amount,
                currency=invoice.total.currency,
                status=invoice.status.value,
            )

            self._session.add(model)
            return

        model.folio = invoice.folio
        model.invoice_date = invoice.invoice_date
        model.total = invoice.total.amount
        model.currency = invoice.total.currency
        model.status = invoice.status.value

    def get_by_id(
        self,
        invoice_id: UUID,
    ) -> Invoice | None:
        model = self._session.get(
            InvoiceModel,
            invoice_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_order_id(
        self,
        order_id: UUID,
    ) -> list[Invoice]:
        statement = select(InvoiceModel).where(
            InvoiceModel.order_id == order_id
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: InvoiceModel,
    ) -> Invoice:
        return Invoice(
            invoice_id=model.id,
            order_id=model.order_id,
            folio=model.folio,
            invoice_date=model.invoice_date,
            total=Money(
                amount=model.total,
                currency=model.currency,
            ),
            status=InvoiceStatus(model.status),
        )