from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository
from src.shared.domain.value_object.rfc import RFC

from .command import ChangeCustomerRFCCommand


class ChangeCustomerRFCHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: ChangeCustomerRFCCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        rfc = RFC(command.new_rfc)

        customer.change_rfc(rfc)

        self._repository.save(customer)