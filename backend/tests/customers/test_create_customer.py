from src.customers.application.create_customer.command import CreateCustomerCommand
from src.customers.application.create_customer.handler import CreateCustomerHandler
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (InMemoryCustomerRepository,)




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