from uuid import uuid4

import pytest

from src.customers.application.change_customer_address.command import (
    ChangeCustomerAddressCommand,
)
from src.customers.application.change_customer_address.handler import (
    ChangeCustomerAddressHandler,
)
from src.customers.application.get_customer.handler import CustomerNotFoundError
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (
    InMemoryCustomerRepository,
)


def test_change_customer_address():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerAddressHandler(repository)

    command = ChangeCustomerAddressCommand(
        customer_id=customer.id,
        street="Av. Patria",
        exterior_number="123",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.address is not None
    assert saved_customer.address.street == "Av. Patria"
    assert saved_customer.address.exterior_number == "123"
    assert saved_customer.address.city == "Calvillo"
    assert saved_customer.address.state == "Aguascalientes"
    assert saved_customer.address.postal_code == "20126"
    assert saved_customer.address.country == "Mexico"


def test_change_customer_address_normalizes_address():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerAddressHandler(repository)

    command = ChangeCustomerAddressCommand(
        customer_id=customer.id,
        street="   Av. Patria   ",
        exterior_number="  123  ",
        city="  Calvillo  ",
        state="  Aguascalientes  ",
        postal_code="  20126  ",
        country="  Mexico  ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.address is not None
    assert saved_customer.address.street == "Av. Patria"
    assert saved_customer.address.exterior_number == "123"
    assert saved_customer.address.city == "Calvillo"
    assert saved_customer.address.state == "Aguascalientes"
    assert saved_customer.address.postal_code == "20126"
    assert saved_customer.address.country == "Mexico"


def test_change_customer_address_supports_optional_fields():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerAddressHandler(repository)

    command = ChangeCustomerAddressCommand(
        customer_id=customer.id,
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

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.address is not None
    assert saved_customer.address.interior_number == "4B"
    assert saved_customer.address.neighborhood == "Centro"


def test_change_customer_address_raises_error_when_address_is_invalid():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerAddressHandler(repository)

    command = ChangeCustomerAddressCommand(
        customer_id=customer.id,
        street="",
        exterior_number="123",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_change_customer_address_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ChangeCustomerAddressHandler(repository)

    command = ChangeCustomerAddressCommand(
        customer_id=uuid4(),
        street="Av. Patria",
        exterior_number="123",
        city="Calvillo",
        state="Aguascalientes",
        postal_code="20126",
        country="Mexico",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)