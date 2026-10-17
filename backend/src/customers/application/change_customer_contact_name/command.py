from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeCustomerContactNameCommand:
    customer_id: UUID
    new_contact_name: str | None