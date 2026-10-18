from src.suppliers.application.list_suppliers.handler import ListSuppliersHandler
from src.suppliers.application.list_suppliers.query import ListSuppliersQuery
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (InMemorySupplierRepository,)


def test_list_suppliers():
    repository = InMemorySupplierRepository()

    repository.save(Supplier("Cliente A"))
    repository.save(Supplier("Cliente B"))
    repository.save(Supplier("Cliente C"))

    handler = ListSuppliersHandler(repository)

    query = ListSuppliersQuery()

    suppliers = handler.execute(query)

    assert len(suppliers) == 3
    assert suppliers[0].name == "Cliente A"
    assert suppliers[1].name == "Cliente B"
    assert suppliers[2].name == "Cliente C"


def test_list_suppliers_returns_empty_list_when_there_are_no_suppliers():
    repository = InMemorySupplierRepository()

    handler = ListSuppliersHandler(repository)

    query = ListSuppliersQuery()

    suppliers = handler.execute(query)

    assert suppliers == []