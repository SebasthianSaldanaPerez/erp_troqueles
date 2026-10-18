from uuid import uuid4

import pytest

from src.customers.application.reactivate_customer.command import (
    ReactivateCustomerCommand,
)
from src.customers.application.reactivate_customer.handler import (
    ReactivateCustomerHandler,
)
from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer import Customer, CustomerStatus

from tests.fakes.in_memory_customer_repository import (InMemoryCustomerRepository,)


def test_reactivate_customer():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    customer.deactivate()
    repository.save(customer)

    handler = ReactivateCustomerHandler(repository)

    command = ReactivateCustomerCommand(
        customer_id=customer.id,
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.status == CustomerStatus.ACTIVE


def test_reactivate_customer_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ReactivateCustomerHandler(repository)

    command = ReactivateCustomerCommand(
        customer_id=uuid4(),
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)