from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository
from src.shared.domain.value_objects.address import Address

from .command import ChangeSupplierAddressCommand


class ChangeSupplierAddressHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: ChangeSupplierAddressCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        address = Address(
            street=command.street,
            exterior_number=command.exterior_number,
            city=command.city,
            state=command.state,
            postal_code=command.postal_code,
            country=command.country,
            interior_number=command.interior_number,
            neighborhood=command.neighborhood,
        )

        supplier.change_address(address)

        self._repository.save(supplier)