from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository
from src.shared.domain.value_objects.phone import Phone

from .command import ChangeSupplierPhoneCommand


class ChangeSupplierPhoneHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: ChangeSupplierPhoneCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        phone = Phone(command.new_phone)

        supplier.change_phone(phone)

        self._repository.save(supplier)