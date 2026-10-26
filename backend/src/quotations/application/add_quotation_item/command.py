from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class AddQuotationItemCommand:
    quotation_id: UUID
    description: str
    quantity: int
    unit_price: Decimal
    currency: str = "MXN"