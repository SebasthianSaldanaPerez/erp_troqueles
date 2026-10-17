from src.customers.domain.customer import Customer
from src.customers.domain.customer_repository import CustomerRepository

from .query import ListCustomersQuery


class ListCustomersHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, query: ListCustomersQuery) -> list[Customer]:
        return self._repository.list_all()