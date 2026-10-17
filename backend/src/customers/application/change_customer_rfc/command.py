from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeCustomerRFCCommand:
    customer_id: UUID
    new_rfc: str