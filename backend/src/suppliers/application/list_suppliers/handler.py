from src.suppliers.domain.supplier import Supplier
from src.suppliers.domain.supplier_repository import SupplierRepository

from .query import ListSuppliersQuery


class ListSuppliersHandler:

    def __init__(self, repository: SupplierRepository):
        self._repository = repository

    def execute(self, query: ListSuppliersQuery) -> list[Supplier]:
        return self._repository.list_all()