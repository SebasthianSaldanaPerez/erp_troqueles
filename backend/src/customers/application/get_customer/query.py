from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetCustomerQuery:
    customer_id: UUID