from src.suppliers.domain.supplier import Supplier
from src.suppliers.domain.supplier_repository import SupplierRepository


class InMemorySupplierRepository(SupplierRepository):

    def __init__(self):
        self.suppliers = []

    def save(self, supplier: Supplier) -> None:
        for index, existing_supplier in enumerate(self.suppliers):
            if existing_supplier.id == supplier.id:
                self.suppliers[index] = supplier
                return

        self.suppliers.append(supplier)

    def get_by_id(self, supplier_id):
        for supplier in self.suppliers:
            if supplier.id == supplier_id:
                return supplier

        return None

    def list_all(self) -> list[Supplier]:
        return list(self.suppliers)