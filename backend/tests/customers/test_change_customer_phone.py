from uuid import uuid4

import pytest

from src.customers.application.change_customer_phone.command import (
    ChangeCustomerPhoneCommand,
)
from src.customers.application.change_customer_phone.handler import (
    ChangeCustomerPhoneHandler,
)
from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (
    InMemoryCustomerRepository,
)
from src.shared.domain.errors import InvalidPhoneError

def test_change_customer_phone():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerPhoneHandler(repository)

    command = ChangeCustomerPhoneCommand(
        customer_id=customer.id,
        new_phone="4494928553",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.phone is not None
    assert saved_customer.phone.value == "4494928553"


def test_change_customer_phone_normalizes_phone():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerPhoneHandler(repository)

    command = ChangeCustomerPhoneCommand(
        customer_id=customer.id,
        new_phone="  4494928553  ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.phone is not None
    assert saved_customer.phone.value == "4494928553"


def test_change_customer_phone_raises_error_when_phone_is_invalid():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerPhoneHandler(repository)

    command = ChangeCustomerPhoneCommand(
        customer_id=customer.id,
        new_phone="INVALID",
    )

    with pytest.raises(InvalidPhoneError):
        handler.execute(command)


def test_change_customer_phone_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ChangeCustomerPhoneHandler(repository)

    command = ChangeCustomerPhoneCommand(
        customer_id=uuid4(),
        new_phone="4494928553",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)