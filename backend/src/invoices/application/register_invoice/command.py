from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class RegisterInvoiceCommand:
    order_id: UUID
    folio: str
    invoice_date: date
    total: Decimal
    currency: str = "MXN"