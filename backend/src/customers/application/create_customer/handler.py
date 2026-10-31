from uuid import UUID

from src.customers.domain.customer import Customer
from src.customers.domain.customer_repository import CustomerRepository

from .command import CreateCustomerCommand
from src.shared.domain.value_objects.address import Address
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.value_objects.rfc import RFC


class CreateCustomerHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, command: CreateCustomerCommand) -> UUID:
        email = Email(command.email) if command.email else None
        rfc = RFC(command.rfc) if command.rfc else None
        phone = Phone(command.phone) if command.phone else None

        address = None

        if command.address_street:
            address = Address(
                street=command.address_street,
                exterior_number=command.address_exterior_number or "",
                interior_number=command.address_interior_number,
                neighborhood=command.address_neighborhood,
                city=command.address_city or "",
                state=command.address_state or "",
                postal_code=command.address_postal_code or "",
                country=command.address_country or "",
            )

        customer = Customer(
            business_name=command.business_name,
            email=email,
            rfc=rfc,
            phone=phone,
            address=address,
            contact_name=command.contact_name,
            notes=command.notes,
        )

        self._repository.save(customer)

        return customer.id