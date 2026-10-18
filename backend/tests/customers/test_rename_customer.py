from uuid import uuid4

import pytest

from tests.fakes.in_memory_customer_repository import (InMemoryCustomerRepository,)
from src.customers.application.errors import CustomerNotFoundError
from src.customers.application.rename_customer.command import RenameCustomerCommand
from src.customers.application.rename_customer.handler import RenameCustomerHandler
from src.customers.domain.customer import Customer
from src.customers.domain.errors import InvalidBusinessNameError



def test_rename_customer():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = RenameCustomerHandler(repository)

    command = RenameCustomerCommand(
        customer_id=customer.id,
        new_business_name="Troqueles Spindola SA de CV",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.business_name == "Troqueles Spindola SA de CV"


def test_rename_customer_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = RenameCustomerHandler(repository)

    command = RenameCustomerCommand(
        customer_id=uuid4(),
        new_business_name="Nuevo Nombre",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)


def test_rename_customer_raises_error_when_new_name_is_empty():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = RenameCustomerHandler(repository)

    command = RenameCustomerCommand(
        customer_id=customer.id,
        new_business_name="",
    )

    with pytest.raises(InvalidBusinessNameError):
        handler.execute(command)