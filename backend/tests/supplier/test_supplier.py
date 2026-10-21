import pytest

from src.suppliers.domain.supplier import Supplier, SupplierStatus
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.rfc import RFC
from src.shared.domain.value_objects.address import Address
from src.shared.domain.value_objects.phone import Phone


def test_supplier_is_created_active():
    supplier = Supplier("Aceros Industriales")

    assert supplier.name == "Aceros Industriales"
    assert supplier.status == SupplierStatus.ACTIVE
    assert supplier.id is not None


def test_supplier_requires_name():
    with pytest.raises(ValueError):
        Supplier("")


def test_supplier_can_be_renamed():
    supplier = Supplier("Aceros Industriales")

    supplier.rename("Aceros Industriales SA de CV")

    assert supplier.name == "Aceros Industriales SA de CV"


def test_supplier_can_be_deactivated():
    supplier = Supplier("Aceros Industriales")

    supplier.deactivate()

    assert supplier.status == SupplierStatus.INACTIVE


def test_supplier_can_be_reactivated():
    supplier = Supplier(
        "Aceros Industriales",
        status=SupplierStatus.INACTIVE,
    )

    supplier.reactivate()

    assert supplier.status == SupplierStatus.ACTIVE

def test_supplier_can_have_email():
    supplier = Supplier(
        "Troqueles Spindola",
        email=Email("ventas@empresa.com"),
    )

    assert supplier.email is not None
    assert supplier.email.value == "ventas@empresa.com"


def test_supplier_can_change_email():
    supplier = Supplier(
        "Troqueles Spindola",
        email=Email("old@empresa.com"),
    )

    supplier.change_email(
        Email("new@empresa.com")
    )

    assert supplier.email is not None
    assert supplier.email.value == "new@empresa.com"


def test_supplier_can_have_rfc():
    supplier = Supplier(
        "Troqueles Spindola",
        rfc=RFC("ABC010203XYZ"),
    )

    assert supplier.rfc is not None
    assert supplier.rfc.value == "ABC010203XYZ"


def test_supplier_can_change_rfc():
    supplier = Supplier(
        "Troqueles Spindola",
        rfc=RFC("OLD010203XYZ"),
    )

    supplier.change_rfc(
        RFC("NEW010203XYZ")
    )

    assert supplier.rfc is not None
    assert supplier.rfc.value == "NEW010203XYZ"


def test_supplier_can_have_address():
    address = Address(
        street="Av. Universidad",
        exterior_number="123",
        city="Aguascalientes",
        state="Aguascalientes",
        postal_code="20000",
        country="Mexico",
    )

    supplier = Supplier(
        "Troqueles Spindola",
        address=address,
    )

    assert supplier.address is not None
    assert supplier.address.street == "Av. Universidad"
    assert supplier.address.city == "Aguascalientes"
    assert supplier.address.postal_code == "20000"

def test_supplier_can_change_address():
    supplier = Supplier(
        "Troqueles Spindola",     
        address = Address(
                street="Av. Patria",
                exterior_number="123",
                city="Calvillo",
                state="Aguascalientes",
                postal_code="20126",
                country="Mexico",
            )
        )

    assert supplier.address is not None
    assert supplier.address.street == "Av. Patria"
    assert supplier.address.city == "Calvillo"
    assert supplier.address.postal_code == "20126"

def test_supplier_can_have_phone():
    supplier = Supplier(
        "Troqueles Spindola",
        phone=Phone("5512345678"),
    )

    assert supplier.phone is not None
    assert supplier.phone.value == "5512345678"

def test_supplier_can_change_phone():
    supplier = Supplier(
        "Troqueles Spindola",
        phone=Phone("5512345678"),
    )

    supplier.change_phone(
        Phone("5587654321")
    )

    assert supplier.phone is not None
    assert supplier.phone.value == "5587654321"

def test_supplier_can_have_contact_name():
    supplier = Supplier(
        "Troqueles Spindola",
        contact_name="John Doe",
    )

    assert supplier.contact_name == "John Doe"

def test_supplier_can_change_contact_name():
    supplier = Supplier(
        "Troqueles Spindola",
        contact_name="John Doe",
    )

    supplier.change_contact_name("Jane Doe")

    assert supplier.contact_name == "Jane Doe"

def test_supplier_can_have_notes():
    supplier = Supplier(
        "Troqueles Spindola",
        notes="Valió madre chavito",
    )

    assert supplier.notes == "Valió madre chavito"

def test_supplier_can_change_notes():
    supplier = Supplier(
        "Troqueles Spindola",
        notes="Valió madre chavito",
    )

    supplier.change_notes("Valió madre chavito, pero ya no tanto")

    assert supplier.notes == "Valió madre chavito, pero ya no tanto"
