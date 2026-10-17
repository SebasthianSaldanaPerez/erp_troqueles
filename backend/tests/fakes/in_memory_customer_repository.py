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

    def list_all(self) -> list[Customer]:
        return list(self.customers)