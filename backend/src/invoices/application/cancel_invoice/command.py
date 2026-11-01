from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CancelInvoiceCommand:
    invoice_id: UUID