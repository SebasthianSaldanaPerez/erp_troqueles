from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from src.suppliers.domain.supplier_repository import SupplierRepository

from .query import GetSupplierQuery


class GetSupplierHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, query: GetSupplierQuery) -> Supplier:
        supplier = self._repository.get_by_id(query.supplier_id)

        if supplier is None:
            raise SupplierNotFoundError(
                f"Supplier {query.supplier_id} was not found"
            )

        return supplier