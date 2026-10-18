from uuid import uuid4

import pytest

from src.suppliers.application.deactivate_supplier.command import (
    DeactivateSupplierCommand,
)
from src.suppliers.application.deactivate_supplier.handler import (
    DeactivateSupplierHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier, SupplierStatus
from tests.fakes.in_memory_supplier_repository import (InMemorySupplierRepository,)


def test_deactivate_supplier():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = DeactivateSupplierHandler(repository)

    command = DeactivateSupplierCommand(
        supplier_id=supplier.id,
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.status == SupplierStatus.INACTIVE


def test_deactivate_supplier_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = DeactivateSupplierHandler(repository)

    command = DeactivateSupplierCommand(
        supplier_id=uuid4(),
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)