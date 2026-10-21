
from uuid import uuid4

import pytest

from src.suppliers.application.change_supplier_phone.command import (
    ChangeSupplierPhoneCommand,
)
from src.suppliers.application.change_supplier_phone.handler import (
    ChangeSupplierPhoneHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)
from src.shared.domain.errors import InvalidPhoneError

def test_change_supplier_phone():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierPhoneHandler(repository)

    command = ChangeSupplierPhoneCommand(
        supplier_id=supplier.id,
        new_phone="4494928553",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.phone is not None
    assert saved_supplier.phone.value == "4494928553"


def test_change_supplier_phone_normalizes_phone():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierPhoneHandler(repository)

    command = ChangeSupplierPhoneCommand(
        supplier_id=supplier.id,
        new_phone="  4494928553  ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.phone is not None
    assert saved_supplier.phone.value == "4494928553"


def test_change_supplier_phone_raises_error_when_phone_is_invalid():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierPhoneHandler(repository)

    command = ChangeSupplierPhoneCommand(
        supplier_id=supplier.id,
        new_phone="INVALID",
    )

    with pytest.raises(InvalidPhoneError):
        handler.execute(command)


def test_change_supplier_phone_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ChangeSupplierPhoneHandler(repository)

    command = ChangeSupplierPhoneCommand(
        supplier_id=uuid4(),
        new_phone="4494928553",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)