from uuid import uuid4

import pytest

from src.suppliers.application.change_supplier_contact_name.command import ChangeSupplierContactNameCommand
from src.suppliers.application.change_supplier_contact_name.handler import (
    ChangeSupplierContactNameHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)


def test_change_supplier_contact_name():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierContactNameHandler(repository)

    command = ChangeSupplierContactNameCommand(
        supplier_id=supplier.id,
        new_contact_name="Nuevo Contacto"
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.contact_name == "Nuevo Contacto"


def test_change_supplier_contact_name_normalizes_contact_name():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierContactNameHandler(repository)

    command = ChangeSupplierContactNameCommand(
        supplier_id=supplier.id,
        new_contact_name="  Nuevo Contacto  ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.contact_name == "Nuevo Contacto"


def test_change_supplier_contact_name_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ChangeSupplierContactNameHandler(repository)

    command = ChangeSupplierContactNameCommand(
        supplier_id=uuid4(),
        new_contact_name="Nuevo Contacto",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)

def test_change_supplier_empty_contact_name():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierContactNameHandler(repository)

    command = ChangeSupplierContactNameCommand(
        supplier_id=supplier.id,
        new_contact_name=None
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.contact_name is None
