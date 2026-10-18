from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository

from .command import DeactivateSupplierCommand


class DeactivateSupplierHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: DeactivateSupplierCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        supplier.deactivate()

        self._repository.save(supplier)