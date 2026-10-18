from uuid import uuid4

import pytest

from src.customers.application.change_customer_contact_name.command import ChangeCustomerContactNameCommand
from src.customers.application.change_customer_contact_name.handler import (
    ChangeCustomerContactNameHandler,
)
from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (
    InMemoryCustomerRepository,
)


def test_change_customer_contact_name():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerContactNameHandler(repository)

    command = ChangeCustomerContactNameCommand(
        customer_id=customer.id,
        new_contact_name="Nuevo Contacto"
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.contact_name == "Nuevo Contacto"


def test_change_customer_contact_name_normalizes_contact_name():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerContactNameHandler(repository)

    command = ChangeCustomerContactNameCommand(
        customer_id=customer.id,
        new_contact_name="  Nuevo Contacto  ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.contact_name == "Nuevo Contacto"


def test_change_customer_contact_name_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ChangeCustomerContactNameHandler(repository)

    command = ChangeCustomerContactNameCommand(
        customer_id=uuid4(),
        new_contact_name="Nuevo Contacto",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)

def test_change_customer_empty_contact_name():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerContactNameHandler(repository)

    command = ChangeCustomerContactNameCommand(
        customer_id=customer.id,
        new_contact_name=None
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.contact_name is None
