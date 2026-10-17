from uuid import uuid4

import pytest

from src.customers.application.change_customer_email.command import (
    ChangeCustomerEmailCommand,
)
from src.customers.application.change_customer_email.handler import (
    ChangeCustomerEmailHandler,
)
from src.customers.application.get_customer.handler import CustomerNotFoundError
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (
    InMemoryCustomerRepository,
)


def test_change_customer_email():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerEmailHandler(repository)

    command = ChangeCustomerEmailCommand(
        customer_id=customer.id,
        new_email="ventas@empresa.com",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.email is not None
    assert saved_customer.email.value == "ventas@empresa.com"


def test_change_customer_email_normalizes_email():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerEmailHandler(repository)

    command = ChangeCustomerEmailCommand(
        customer_id=customer.id,
        new_email="  VENTAS@EMPRESA.COM  ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.email is not None
    assert saved_customer.email.value == "ventas@empresa.com"


def test_change_customer_email_raises_error_when_email_is_invalid():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerEmailHandler(repository)

    command = ChangeCustomerEmailCommand(
        customer_id=customer.id,
        new_email="invalid-email",
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_change_customer_email_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ChangeCustomerEmailHandler(repository)

    command = ChangeCustomerEmailCommand(
        customer_id=uuid4(),
        new_email="ventas@empresa.com",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)