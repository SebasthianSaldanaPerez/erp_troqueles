from src.suppliers.application.create_supplier.command import (
    CreateSupplierCommand,
)
from src.suppliers.application.create_supplier.handler import (
    CreateSupplierHandler,
)
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)


def test_create_supplier():
    repository = InMemorySupplierRepository()
    handler = CreateSupplierHandler(repository)

    command = CreateSupplierCommand(
        name="Aceros Industriales",
    )

    supplier_id = handler.execute(command)

    saved_supplier = repository.get_by_id(supplier_id)

    assert supplier_id is not None
    assert saved_supplier is not None
    assert saved_supplier.name == "Aceros Industriales"