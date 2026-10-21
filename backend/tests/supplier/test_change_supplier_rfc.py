from uuid import uuid4

import pytest

from src.suppliers.application.change_supplier_rfc.command import (
    ChangeSupplierRFCCommand,
)
from src.suppliers.application.change_supplier_rfc.handler import (
    ChangeSupplierRFCHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)
from src.shared.domain.errors import InvalidRFCError

def test_change_supplier_rfc():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierRFCHandler(repository)

    command = ChangeSupplierRFCCommand(
        supplier_id=supplier.id,
        new_rfc="ABC010203XYZ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.rfc is not None
    assert saved_supplier.rfc.value == "ABC010203XYZ"


def test_change_supplier_rfc_normalizes_rfc():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierRFCHandler(repository)

    command = ChangeSupplierRFCCommand(
        supplier_id=supplier.id,
        new_rfc="  abc010203xyz  ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.rfc is not None
    assert saved_supplier.rfc.value == "ABC010203XYZ"


def test_change_supplier_rfc_raises_error_when_rfc_is_invalid():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierRFCHandler(repository)

    command = ChangeSupplierRFCCommand(
        supplier_id=supplier.id,
        new_rfc="INVALID",
    )

    with pytest.raises(InvalidRFCError):
        handler.execute(command)


def test_change_supplier_rfc_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ChangeSupplierRFCHandler(repository)

    command = ChangeSupplierRFCCommand(
        supplier_id=uuid4(),
        new_rfc="ABC010203XYZ",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)