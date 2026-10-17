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


class InMemoryCustomerRepository(CustomerRepository):

    def __init__(self):
        self.customers = []

    def save(self, customer: Customer) -> None:
        for index, existing_customer in enumerate(self.customers):
            if existing_customer.id == customer.id:
                self.customers[index] = customer
                return

        self.customers.append(customer)

    def get_by_id(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer

        return None


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