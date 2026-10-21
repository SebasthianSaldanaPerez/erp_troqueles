from src.customers.application.errors import CustomerNotFoundError
from src.customers.domain.customer_repository import CustomerRepository
from src.shared.domain.value_objects.address import Address

from .command import ChangeCustomerAddressCommand


class ChangeCustomerAddressHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: ChangeCustomerAddressCommand) -> None:
        customer = self._repository.get_by_id(command.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {command.customer_id} was not found"
            )

        address = Address(
            street=command.street,
            exterior_number=command.exterior_number,
            city=command.city,
            state=command.state,
            postal_code=command.postal_code,
            country=command.country,
            interior_number=command.interior_number,
            neighborhood=command.neighborhood,
        )

        customer.change_address(address)

        self._repository.save(customer)