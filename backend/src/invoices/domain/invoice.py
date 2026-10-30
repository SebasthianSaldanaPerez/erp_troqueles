from datetime import date
from enum import Enum
from uuid import UUID, uuid4

from src.shared.domain.value_objects.money import Money


class InvoiceStatus(Enum):
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"


class Invoice:
    def __init__(
        self,
        order_id: UUID,
        folio: str,
        invoice_date: date,
        total: Money,
        invoice_id: UUID | None = None,
        status: InvoiceStatus = InvoiceStatus.REGISTERED,
    ):
        self._id = invoice_id or uuid4()
        self._order_id = order_id
        self._folio = self._validate_folio(folio)
        self._invoice_date = invoice_date
        self._total = total
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def order_id(self) -> UUID:
        return self._order_id

    @property
    def folio(self) -> str:
        return self._folio

    @property
    def invoice_date(self) -> date:
        return self._invoice_date

    @property
    def total(self) -> Money:
        return self._total

    @property
    def status(self) -> InvoiceStatus:
        return self._status

    def cancel(self) -> None:
        if self._status == InvoiceStatus.CANCELLED:
            raise ValueError("Invoice is already cancelled")

        self._status = InvoiceStatus.CANCELLED

    @staticmethod
    def _validate_folio(folio: str) -> str:
        if not folio or not folio.strip():
            raise ValueError("Invoice folio is required")

        return folio.strip()