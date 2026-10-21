import pytest

from src.shared.domain.value_objects.address import Address
from src.shared.domain.errors import InvalidAddressError


def test_address_is_created():
    address = Address(
        street="Av. Universidad",
        exterior_number="123",
        city="Aguascalientes",
        state="Aguascalientes",
        postal_code="20000",
        country="Mexico",
    )

    assert address.street == "Av. Universidad"
    assert address.exterior_number == "123"
    assert address.city == "Aguascalientes"


def test_address_is_normalized():
    address = Address(
        street="  Av. Universidad  ",
        exterior_number="  123  ",
        city="  Aguascalientes  ",
        state="  Aguascalientes  ",
        postal_code="  20000  ",
        country="  Mexico  ",
    )

    assert address.street == "Av. Universidad"
    assert address.exterior_number == "123"
    assert address.postal_code == "20000"


def test_address_requires_street():
    with pytest.raises(InvalidAddressError):
        Address(
            street="",
            exterior_number="123",
            city="Aguascalientes",
            state="Aguascalientes",
            postal_code="20000",
            country="Mexico",
        )


def test_address_requires_city():
    with pytest.raises(InvalidAddressError):
        Address(
            street="Av. Universidad",
            exterior_number="123",
            city="",
            state="Aguascalientes",
            postal_code="20000",
            country="Mexico",
        )