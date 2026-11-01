from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetOrderQuery:
    order_id: UUID