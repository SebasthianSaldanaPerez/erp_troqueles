from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CancelQuotationCommand:
    quotation_id: UUID