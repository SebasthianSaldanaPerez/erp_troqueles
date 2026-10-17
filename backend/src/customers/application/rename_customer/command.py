from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RenameCustomerCommand:
    customer_id: UUID
    new_business_name: str