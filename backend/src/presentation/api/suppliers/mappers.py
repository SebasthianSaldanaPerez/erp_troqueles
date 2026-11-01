from src.presentation.api.suppliers.schemas import (
    AddressResponse,
    SupplierResponse,
)
from src.suppliers.domain.supplier import Supplier


def supplier_to_response(supplier: Supplier) -> SupplierResponse:
    address = None

    if supplier.address is not None:
        address = AddressResponse(
            street=supplier.address.street,
            exterior_number=supplier.address.exterior_number,
            interior_number=supplier.address.interior_number,
            neighborhood=supplier.address.neighborhood,
            city=supplier.address.city,
            state=supplier.address.state,
            postal_code=supplier.address.postal_code,
            country=supplier.address.country,
        )

    return SupplierResponse(
        id=str(supplier.id),
        name=supplier.name,
        status=supplier.status.value,
        email=supplier.email.value if supplier.email else None,
        rfc=supplier.rfc.value if supplier.rfc else None,
        phone=supplier.phone.value if supplier.phone else None,
        address=address,
        contact_name=supplier.contact_name,
        notes=supplier.notes,
    )