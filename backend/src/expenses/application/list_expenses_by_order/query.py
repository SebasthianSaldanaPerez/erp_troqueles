from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ListExpensesByOrderQuery:
    order_id: UUID