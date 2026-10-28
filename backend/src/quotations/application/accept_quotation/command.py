from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AcceptQuotationCommand:
    quotation_id: UUID