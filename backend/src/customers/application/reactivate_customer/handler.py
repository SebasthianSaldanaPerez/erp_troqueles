from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository

from .command import ReactivateCustomerCommand


class ReactivateCustomerHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: ReactivateCustomerCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        customer.reactivate()

        self._repository.save(customer)