from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SendQuotationCommand:
    quotation_id: UUID