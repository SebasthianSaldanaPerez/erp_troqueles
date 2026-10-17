from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeCustomerEmailCommand:
    customer_id: UUID
    new_email: str