from uuid import uuid4

import pytest

from src.customers.application.change_customer_notes.command import ChangeCustomerNotesCommand
from src.customers.application.change_customer_notes.handler import (
    ChangeCustomerNotesHandler,
)
from src.customers.application.get_customer.handler import CustomerNotFoundError
from src.customers.domain.customer import Customer
from tests.fakes.in_memory_customer_repository import (
    InMemoryCustomerRepository,
)


def test_change_customer_notes():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerNotesHandler(repository)

    command = ChangeCustomerNotesCommand(
        customer_id=customer.id,
        new_notes="Nuevas notas"
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.notes == "Nuevas notas"


def test_change_customer_notes_normalizes_notes():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerNotesHandler(repository)

    command = ChangeCustomerNotesCommand(
        customer_id=customer.id,
        new_notes="  Nuevas notas  ",
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.notes == "Nuevas notas"


def test_change_customer_notes_raises_error_when_customer_does_not_exist():
    repository = InMemoryCustomerRepository()

    handler = ChangeCustomerNotesHandler(repository)

    command = ChangeCustomerNotesCommand(
        customer_id=uuid4(),
        new_notes="Nuevas notas",
    )

    with pytest.raises(CustomerNotFoundError):
        handler.execute(command)

def test_change_customer_empty_notes():
    repository = InMemoryCustomerRepository()

    customer = Customer("Troqueles Spindola")
    repository.save(customer)

    handler = ChangeCustomerNotesHandler(repository)

    command = ChangeCustomerNotesCommand(
        customer_id=customer.id,
        new_notes=None
    )

    handler.execute(command)

    saved_customer = repository.get_by_id(customer.id)

    assert saved_customer is not None
    assert saved_customer.notes is None
