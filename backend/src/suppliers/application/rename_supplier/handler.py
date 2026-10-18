from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier_repository import SupplierRepository

from .command import RenameSupplierCommand


class RenameSupplierHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: RenameSupplierCommand) -> None:
        supplier = self._repository.get_by_id(command.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {command.supplier_id} was not found"
            )

        supplier.rename(command.new_name)

        self._repository.save(supplier)