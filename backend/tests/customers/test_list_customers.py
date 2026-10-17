from src.customers.application.list_customers.handler import ListCustomersHandler
from src.customers.application.list_customers.query import ListCustomersQuery
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (InMemoryCustomerRepository,)


def test_list_customers():
    repository = InMemoryCustomerRepository()

    repository.save(Customer("Cliente A"))
    repository.save(Customer("Cliente B"))
    repository.save(Customer("Cliente C"))

    handler = ListCustomersHandler(repository)

    query = ListCustomersQuery()

    customers = handler.execute(query)

    assert len(customers) == 3
    assert customers[0].business_name == "Cliente A"
    assert customers[1].business_name == "Cliente B"
    assert customers[2].business_name == "Cliente C"


def test_list_customers_returns_empty_list_when_there_are_no_customers():
    repository = InMemoryCustomerRepository()

    handler = ListCustomersHandler(repository)

    query = ListCustomersQuery()

    customers = handler.execute(query)

    assert customers == []