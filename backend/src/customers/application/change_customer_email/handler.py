from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository
from src.customers.domain.value_objects.email import Email

from .command import ChangeCustomerEmailCommand


class ChangeCustomerEmailHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: ChangeCustomerEmailCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        email = Email(command.new_email)

        customer.change_email(email)

        self._repository.save(customer)