from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetQuotationQuery:
    quotation_id: UUID