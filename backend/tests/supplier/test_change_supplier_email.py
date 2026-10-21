from uuid import uuid4

import pytest

from src.suppliers.application.change_supplier_email.command import (
    ChangeSupplierEmailCommand,
)
from src.suppliers.application.change_supplier_email.handler import (
    ChangeSupplierEmailHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)
from src.shared.domain.errors import InvalidEmailError

def test_change_supplier_email():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierEmailHandler(repository)

    command = ChangeSupplierEmailCommand(
        supplier_id=supplier.id,
        new_email="ventas@empresa.com",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.email is not None
    assert saved_supplier.email.value == "ventas@empresa.com"


def test_change_supplier_email_normalizes_email():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierEmailHandler(repository)

    command = ChangeSupplierEmailCommand(
        supplier_id=supplier.id,
        new_email="  VENTAS@EMPRESA.COM  ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.email is not None
    assert saved_supplier.email.value == "ventas@empresa.com"


def test_change_supplier_email_raises_error_when_email_is_invalid():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierEmailHandler(repository)

    command = ChangeSupplierEmailCommand(
        supplier_id=supplier.id,
        new_email="invalid-email",
    )

    with pytest.raises(InvalidEmailError):
        handler.execute(command)


def test_change_supplier_email_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ChangeSupplierEmailHandler(repository)

    command = ChangeSupplierEmailCommand(
        supplier_id=uuid4(),
        new_email="ventas@empresa.com",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)