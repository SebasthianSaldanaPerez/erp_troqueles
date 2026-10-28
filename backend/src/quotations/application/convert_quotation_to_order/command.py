from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ConvertQuotationToOrderCommand:
    quotation_id: UUID