from uuid import uuid4

import pytest

from src.suppliers.application.change_supplier_address.command import (
    ChangeSupplierAddressCommand,
)
from src.suppliers.application.change_supplier_address.handler import (
    ChangeSupplierAddressHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.domain.supplier import Supplier
from tests.fakes.in_memory_supplier_repository import (
    InMemorySupplierRepository,
)
from src.shared.domain.errors import InvalidAddressError


def test_change_supplier_address():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierAddressHandler(repository)

    command = ChangeSupplierAddressCommand(
        supplier_id=supplier.id,
        street="Av. Patria",
        exterior_number="123",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.address is not None
    assert saved_supplier.address.street == "Av. Patria"
    assert saved_supplier.address.exterior_number == "123"
    assert saved_supplier.address.city == "Calvillo"
    assert saved_supplier.address.state == "Aguascalientes"
    assert saved_supplier.address.postal_code == "20126"
    assert saved_supplier.address.country == "Mexico"


def test_change_supplier_address_normalizes_address():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierAddressHandler(repository)

    command = ChangeSupplierAddressCommand(
        supplier_id=supplier.id,
        street="   Av. Patria   ",
        exterior_number="  123  ",
        city="  Calvillo  ",
        state="  Aguascalientes  ",
        postal_code="  20126  ",
        country="  Mexico  ",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.address is not None
    assert saved_supplier.address.street == "Av. Patria"
    assert saved_supplier.address.exterior_number == "123"
    assert saved_supplier.address.city == "Calvillo"
    assert saved_supplier.address.state == "Aguascalientes"
    assert saved_supplier.address.postal_code == "20126"
    assert saved_supplier.address.country == "Mexico"


def test_change_supplier_address_supports_optional_fields():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierAddressHandler(repository)

    command = ChangeSupplierAddressCommand(
        supplier_id=supplier.id,
        street="Av. Patria",
        exterior_number="123",
        interior_number="4B",
        neighborhood="Centro",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    handler.execute(command)

    saved_supplier = repository.get_by_id(supplier.id)

    assert saved_supplier is not None
    assert saved_supplier.address is not None
    assert saved_supplier.address.interior_number == "4B"
    assert saved_supplier.address.neighborhood == "Centro"


def test_change_supplier_address_raises_error_when_address_is_invalid():
    repository = InMemorySupplierRepository()

    supplier = Supplier("Troqueles Spindola")
    repository.save(supplier)

    handler = ChangeSupplierAddressHandler(repository)

    command = ChangeSupplierAddressCommand(
        supplier_id=supplier.id,
        street="",
        exterior_number="123",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    with pytest.raises(InvalidAddressError):
        handler.execute(command)


def test_change_supplier_address_raises_error_when_supplier_does_not_exist():
    repository = InMemorySupplierRepository()

    handler = ChangeSupplierAddressHandler(repository)

    command = ChangeSupplierAddressCommand(
        supplier_id=uuid4(),
        street="Av. Patria",
        exterior_number="123",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    with pytest.raises(SupplierNotFoundError):
        handler.execute(command)