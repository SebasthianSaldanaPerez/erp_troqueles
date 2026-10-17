from src.customers.domain.customer import Customer
from src.customers.domain.customer_repository import CustomerRepository

from .query import GetCustomerQuery


class CustomerNotFoundError(Exception):
    pass


class GetCustomerHandler:

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    def execute(self, query: GetCustomerQuery) -> Customer:
        customer = self._repository.get_by_id(query.customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer {query.customer_id} was not found"
            )

        return customer