from uuid import uuid4

import pytest

from src.customers.application.get_customer.handler import (
    CustomerNotFoundError,
    GetCustomerHandler,
)
from src.customers.application.get_customer.query import GetCustomerQuery
from src.customers.domain.customer import Customer
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


def test_get_customer():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = GetCustomerHandler(repository)

    query = GetCustomerQuery(
        customer_id=customer.id,
    )

    result = handler.execute(query)

    assert result.id == customer.id
    assert result.business_name == "Troqueles Spindola"


def test_get_customer_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()
    handler = GetCustomerHandler(repository)

    query = GetCustomerQuery(
        customer_id=uuid4(),
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(query)