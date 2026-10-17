from uuid import uuid4

import pytest

from src.customers.application.deactivate_customer.command import (
    DeactivateCustomerCommand,
)
from src.customers.application.deactivate_customer.handler import (
    DeactivateCustomerHandler,
)
from src.customers.application.get_customer.handler import CustomerNotFoundError
from src.customers.domain.customer import Customer, CustomerStatus
from src.customers.domain.customer_repository import CustomerRepository
from tests.fakes.in_memory_customer_repository import (InMemoryCustomerRepository,)


def test_deactivate_customer():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = DeactivateCustomerHandler(repository)

    command = DeactivateCustomerCommand(
        customer_id=customer.id,
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.status == CustomerStatus.INACTIVE


def test_deactivate_customer_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = DeactivateCustomerHandler(repository)

    command = DeactivateCustomerCommand(
        customer_id=uuid4(),
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)