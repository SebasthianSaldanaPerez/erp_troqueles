from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class CreateQuotationCommand:
    customer_id: UUID
    tax_rate: Decimal
    currency: str = "MXN"