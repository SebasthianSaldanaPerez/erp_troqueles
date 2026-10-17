from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ReactivateCustomerCommand:
    customer_id: UUID