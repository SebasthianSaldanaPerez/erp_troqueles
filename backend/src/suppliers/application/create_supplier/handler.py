from uuid import UUID

from src.suppliers.domain.supplier import Supplier
from src.suppliers.domain.supplier_repository import SupplierRepository

from .command import CreateSupplierCommand


class CreateSupplierHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, command: CreateSupplierCommand) -> UUID:
        supplier = Supplier(
            name=command.name,
        )

        self._repository.save(supplier)

        return supplier.id