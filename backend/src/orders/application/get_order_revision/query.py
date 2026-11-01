from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetOrderRevisionQuery:
    order_id: UUID
    revision_number: int