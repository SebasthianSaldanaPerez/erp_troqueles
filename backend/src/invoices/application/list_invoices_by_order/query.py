from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ListInvoicesByOrderQuery:
    order_id: UUID