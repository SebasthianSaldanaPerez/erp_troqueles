from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeliverOrderCommand:
    order_id: UUID