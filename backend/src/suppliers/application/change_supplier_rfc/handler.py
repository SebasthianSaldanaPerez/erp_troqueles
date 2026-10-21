from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository
from src.shared.domain.value_objects.rfc import RFC

from .command import ChangeSupplierRFCCommand


class ChangeSupplierRFCHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: ChangeSupplierRFCCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        rfc = RFC(command.new_rfc)

        supplier.change_rfc(rfc)

        self._repository.save(supplier)