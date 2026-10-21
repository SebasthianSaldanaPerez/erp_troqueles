from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository
from .command import ChangeSupplierContactNameCommand


class ChangeSupplierContactNameHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: ChangeSupplierContactNameCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        contact_name = command.new_contact_name

        supplier.change_contact_name(contact_name)

        self._repository.save(supplier)