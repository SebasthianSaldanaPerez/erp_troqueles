from uuid import uuid4

import pytest

from tests.fakes.in_memory_supplier_repository import (InMemorySupplierRepository,)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.application.rename_supplier.command import RenameSupplierCommand
from src.suppliers.application.rename_supplier.handler import RenameSupplierHandler
from src.suppliers.domain.supplier import Supplier
from src.suppliers.domain.errors import InvalidSupplierNameError



def test_rename_supplier():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = RenameSupplierHandler(repository)

    command = RenameSupplierCommand(
        supplier_id=supplier.id,
        new_name="Troqueles Spindola SA de CV",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.name == "Troqueles Spindola SA de CV"


def test_rename_supplier_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = RenameSupplierHandler(repository)

    command = RenameSupplierCommand(
        supplier_id=uuid4(),
        new_name="Nuevo Nombre",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)


def test_rename_supplier_raises_error_when_new_name_is_empty():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = RenameSupplierHandler(repository)

    command = RenameSupplierCommand(
        supplier_id=supplier.id,
        new_name="",
    )

    with pytest.raises(InvalidSupplierNameError):
        handler.execute(command)