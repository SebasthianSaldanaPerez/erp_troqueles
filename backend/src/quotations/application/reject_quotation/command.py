from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RejectQuotationCommand:
    quotation_id: UUID