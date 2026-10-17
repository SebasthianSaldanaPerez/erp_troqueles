from src.customers.application.get_customer.handler import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository

from .command import DeactivateCustomerCommand


class DeactivateCustomerHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: DeactivateCustomerCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        customer.deactivate()

        self._repository.save(customer)