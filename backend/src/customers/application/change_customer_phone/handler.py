from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository
from src.shared.domain.value_objects.phone import Phone

from .command import ChangeCustomerPhoneCommand


class ChangeCustomerPhoneHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: ChangeCustomerPhoneCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        phone = Phone(command.new_phone)

        customer.change_phone(phone)

        self._repository.save(customer)