from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RemoveQuotationItemCommand:
    quotation_id: UUID
    item_id: UUID