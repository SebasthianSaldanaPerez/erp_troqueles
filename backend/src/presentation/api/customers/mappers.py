from src.customers.domain.customer import Customer
from src.presentation.api.customers.schemas import (
    AddressResponse,
    CustomerResponse,
)


def customer_to_response(customer: Customer) -> CustomerResponse:
    address = None

    if customer.address is not None:
        address = AddressResponse(
            street=customer.address.street,
            exterior_number=customer.address.exterior_number,
            interior_number=customer.address.interior_number,
            neighborhood=customer.address.neighborhood,
            city=customer.address.city,
            state=customer.address.state,
            postal_code=customer.address.postal_code,
            country=customer.address.country,
        )

    return CustomerResponse(
        id=str(customer.id),
        business_name=customer.business_name,
        status=customer.status.value,
        email=customer.email.value if customer.email else None,
        rfc=customer.rfc.value if customer.rfc else None,
        phone=customer.phone.value if customer.phone else None,
        address=address,
        contact_name=customer.contact_name,
        notes=customer.notes,
    )