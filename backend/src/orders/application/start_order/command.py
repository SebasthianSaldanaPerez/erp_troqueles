from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class StartOrderCommand:
    order_id: UUID