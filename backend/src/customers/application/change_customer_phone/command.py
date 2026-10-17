from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeCustomerPhoneCommand:
    customer_id: UUID
    new_phone: str