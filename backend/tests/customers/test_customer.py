from src.customers.domain.value_objects.address import Address
from src.customers.domain.value_objects.phone import Phone

import pytest
from src.customers.domain.customer import Customer, CustomerStatus
from src.customers.domain.value_objects.email import Email
from src.customers.domain.value_objects.rfc import RFC

def test_customer_is_created_active():
    customer = Customer("Troqueles Spindola")

    assert customer.business_name == "Troqueles Spindola"
    assert customer.status == CustomerStatus.ACTIVE
    assert customer.id is not None


def test_customer_requires_business_name():
    with pytest.raises(ValueError):
        Customer("")

def test_customer_can_be_renamed():
    customer = Customer("Troqueles Spindola")

    customer.rename("Troqueles Spindola SA de CV")

    assert customer.business_name == "Troqueles Spindola SA de CV"


def test_customer_cannot_be_renamed_with_empty_name():
    customer = Customer("Troqueles Spindola")

    with pytest.raises(ValueError):
        customer.rename("")


def test_customer_can_be_deactivated():
    customer = Customer("Troqueles Spindola")

    customer.deactivate()

    assert customer.status == CustomerStatus.INACTIVE


def test_customer_can_be_reactivated():
    customer = Customer(
        "Troqueles Spindola",
        status=CustomerStatus.INACTIVE,
    )

    customer.reactivate()

    assert customer.status == CustomerStatus.ACTIVE

def test_customer_can_have_email():
    customer = Customer(
        "Troqueles Spindola",
        email=Email("ventas@empresa.com"),
    )

    assert customer.email is not None
    assert customer.email.value == "ventas@empresa.com"


def test_customer_can_change_email():
    customer = Customer(
        "Troqueles Spindola",
        email=Email("old@empresa.com"),
    )

    customer.change_email(
        Email("new@empresa.com")
    )

    assert customer.email is not None
    assert customer.email.value == "new@empresa.com"


def test_customer_can_have_rfc():
    customer = Customer(
        "Troqueles Spindola",
        rfc=RFC("ABC010203XYZ"),
    )

    assert customer.rfc is not None
    assert customer.rfc.value == "ABC010203XYZ"


def test_customer_can_change_rfc():
    customer = Customer(
        "Troqueles Spindola",
        rfc=RFC("OLD010203XYZ"),
    )

    customer.change_rfc(
        RFC("NEW010203XYZ")
    )

    assert customer.rfc is not None
    assert customer.rfc.value == "NEW010203XYZ"


def test_customer_can_have_address():
    address = Address(
        street="Av. Universidad",
        exterior_number="123",
        city="Aguascalientes",
        state="Aguascalientes",
        postal_code="20000",
        country="Mexico",
    )

    customer = Customer(
        "Troqueles Spindola",
        address=address,
    )

    assert customer.address is not None
    assert customer.address.street == "Av. Universidad"
    assert customer.address.city == "Aguascalientes"
    assert customer.address.postal_code == "20000"

def test_customer_can_change_address():
    customer = Customer(
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

    assert customer.address is not None
    assert customer.address.street == "Av. Patria"
    assert customer.address.city == "Calvillo"
    assert customer.address.postal_code == "20126"

def test_customer_can_have_phone():
    customer = Customer(
        "Troqueles Spindola",
        phone=Phone("5512345678"),
    )

    assert customer.phone is not None
    assert customer.phone.value == "5512345678"

def test_customer_can_change_phone():
    customer = Customer(
        "Troqueles Spindola",
        phone=Phone("5512345678"),
    )

    customer.change_phone(
        Phone("5587654321")
    )

    assert customer.phone is not None
    assert customer.phone.value == "5587654321"

def test_customer_can_have_contact_name():
    customer = Customer(
        "Troqueles Spindola",
        contact_name="John Doe",
    )

    assert customer.contact_name == "John Doe"

def test_customer_can_change_contact_name():
    customer = Customer(
        "Troqueles Spindola",
        contact_name="John Doe",
    )

    customer.change_contact_name("Jane Doe")

    assert customer.contact_name == "Jane Doe"

def test_customer_can_have_notes():
    customer = Customer(
        "Troqueles Spindola",
        notes="Valió madre chavito",
    )

    assert customer.notes == "Valió madre chavito"

def test_customer_can_change_notes():
    customer = Customer(
        "Troqueles Spindola",
        notes="Valió madre chavito",
    )

    customer.change_notes("Valió madre chavito, pero ya no tanto")

    assert customer.notes == "Valió madre chavito, pero ya no tanto"
