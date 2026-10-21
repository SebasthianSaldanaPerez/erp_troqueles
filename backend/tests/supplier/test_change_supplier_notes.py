from uuid import uuid4

import pytest

from src.suppliers.application.change_supplier_notes.command import ChangeSupplierNotesCommand
from src.suppliers.application.change_supplier_notes.handler import (
    ChangeSupplierNotesHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)


def test_change_supplier_notes():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierNotesHandler(repository)

    command = ChangeSupplierNotesCommand(
        supplier_id=supplier.id,
        new_notes="Nuevas notas"
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.notes == "Nuevas notas"


def test_change_supplier_notes_normalizes_notes():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierNotesHandler(repository)

    command = ChangeSupplierNotesCommand(
        supplier_id=supplier.id,
        new_notes="  Nuevas notas  ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.notes == "Nuevas notas"


def test_change_supplier_notes_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ChangeSupplierNotesHandler(repository)

    command = ChangeSupplierNotesCommand(
        supplier_id=uuid4(),
        new_notes="Nuevas notas",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)

def test_change_supplier_empty_notes():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierNotesHandler(repository)

    command = ChangeSupplierNotesCommand(
        supplier_id=supplier.id,
        new_notes=None
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.notes is None
