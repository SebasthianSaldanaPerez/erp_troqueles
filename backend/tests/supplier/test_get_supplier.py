from uuid import uuid4

import pytest

from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.application.get_supplier.handler import (
    GetSupplierHandler,
)
from src.suppliers.application.get_supplier.query import GetSupplierQuery
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


def test_get_supplier():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = GetSupplierHandler(repository)

    query = GetSupplierQuery(
        supplier_id=supplier.id,
    )

    result = handler.execute(query)

    assert result.id == supplier.id
    assert result.name == "Troqueles Spindola"


def test_get_supplier_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()
    handler = GetSupplierHandler(repository)

    query = GetSupplierQuery(
        supplier_id=uuid4(),
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(query)