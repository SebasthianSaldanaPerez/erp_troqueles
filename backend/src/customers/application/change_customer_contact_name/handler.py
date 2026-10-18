from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository
from .command import ChangeCustomerContactNameCommand


class ChangeCustomerContactNameHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: ChangeCustomerContactNameCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        contact_name = command.new_contact_name

        customer.change_contact_name(contact_name)

        self._repository.save(customer)