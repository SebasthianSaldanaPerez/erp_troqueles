from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeCustomerAddressCommand:
    customer_id: UUID
    street: str
    exterior_number: str
    city: str
    state: str
    postal_code: str
    country: str
    interior_number: str | None = None
    neighborhood: str | None = None