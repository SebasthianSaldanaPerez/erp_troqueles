from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ListDocumentsByOrderQuery:
    order_id: UUID