from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class ReviseOrderCommand:
    order_id: UUID
    item_id: UUID
    description: str
    quantity: int
    unit_price: Decimal
    currency: str
    reason: str
    user_id: UUID