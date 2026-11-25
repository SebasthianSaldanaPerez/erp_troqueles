from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ReopenQuotationCommand:
    quotation_id: UUID