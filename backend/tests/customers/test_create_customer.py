from src.customers.application.create_customer.command import CreateCustomerCommand
from src.customers.application.create_customer.handler import CreateCustomerHandler
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


def test_create_customer():
    repository = InMemoryCustomerRepository()
    handler = CreateCustomerHandler(repository)

    command = CreateCustomerCommand(
        business_name="Troqueles Spindola",
    )

    customer_id = handler.execute(command)

    assert customer_id is not None
    assert len(repository.customers) == 1
    assert repository.customers[0].business_name == "Troqueles Spindola"