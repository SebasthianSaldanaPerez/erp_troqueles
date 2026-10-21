from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository
from src.shared.domain.value_objects.email import Email

from .command import ChangeSupplierEmailCommand


class ChangeSupplierEmailHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: ChangeSupplierEmailCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        email = Email(command.new_email)

        supplier.change_email(email)

        self._repository.save(supplier)