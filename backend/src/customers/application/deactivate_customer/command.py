from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeactivateCustomerCommand:
    customer_id: UUID