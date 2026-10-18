from uuid import uuid4

import pytest

from src.customers.application.change_customer_rfc.command import (
    ChangeCustomerRFCCommand,
)
from src.customers.application.change_customer_rfc.handler import (
    ChangeCustomerRFCHandler,
)
from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (
    InMemoryCustomerRepository,
)
from src.customers.domain.errors import InvalidRFCError

def test_change_customer_rfc():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerRFCHandler(repository)

    command = ChangeCustomerRFCCommand(
        customer_id=customer.id,
        new_rfc="ABC010203XYZ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.rfc is not None
    assert saved_customer.rfc.value == "ABC010203XYZ"


def test_change_customer_rfc_normalizes_rfc():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerRFCHandler(repository)

    command = ChangeCustomerRFCCommand(
        customer_id=customer.id,
        new_rfc="  abc010203xyz  ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.rfc is not None
    assert saved_customer.rfc.value == "ABC010203XYZ"


def test_change_customer_rfc_raises_error_when_rfc_is_invalid():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerRFCHandler(repository)

    command = ChangeCustomerRFCCommand(
        customer_id=customer.id,
        new_rfc="INVALID",
    )

    with pytest.raises(InvalidRFCError):
        handler.execute(command)


def test_change_customer_rfc_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ChangeCustomerRFCHandler(repository)

    command = ChangeCustomerRFCCommand(
        customer_id=uuid4(),
        new_rfc="ABC010203XYZ",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)