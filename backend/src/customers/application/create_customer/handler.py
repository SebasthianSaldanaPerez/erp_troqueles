from uuid import UUID

from src.customers.domain.customer import Customer
from src.customers.domain.customer_repository import CustomerRepository

from .command import CreateCustomerCommand


class CreateCustomerHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: CreateCustomerCommand) -> UUID:
        customer = Customer(
            business_name=command.business_name,
        )

        self._repository.save(customer)

        return customer.id