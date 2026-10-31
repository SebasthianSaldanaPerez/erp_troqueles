from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCustomerCommand:
    business_name: str
    email: str | None = None
    rfc: str | None = None
    phone: str | None = None

    address_street: str | None = None
    address_exterior_number: str | None = None
    address_interior_number: str | None = None
    address_neighborhood: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_postal_code: str | None = None
    address_country: str | None = None

    contact_name: str | None = None
    notes: str | None = None