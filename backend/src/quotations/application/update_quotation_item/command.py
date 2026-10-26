from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class UpdateQuotationItemCommand:
    quotation_id: UUID
    item_id: UUID
    description: str
    quantity: int
    unit_price: Decimal
    currency: str = "MXN"