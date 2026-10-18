from uuid import uuid4

import pytest

from src.suppliers.application.reactivate_supplier.command import (
    ReactivateSupplierCommand,
)
from src.suppliers.application.reactivate_supplier.handler import (
    ReactivateSupplierHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier, SupplierStatus

from tests.fakes.in_memory_supplier_repository import (InMemorySupplierRepository,)


def test_reactivate_supplier():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    supplier.deactivate()
    repository.save(supplier)

    handler = ReactivateSupplierHandler(repository)

    command = ReactivateSupplierCommand(
        supplier_id=supplier.id,
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.status == SupplierStatus.ACTIVE


def test_reactivate_supplier_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ReactivateSupplierHandler(repository)

    command = ReactivateSupplierCommand(
        supplier_id=uuid4(),
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)