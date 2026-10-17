import pytest
from src.customers.domain.customer import Customer, CustomerStatus


def test_customer_is_created_active():
    customer = Customer("Troqueles Spindola")

    assert customer.business_name == "Troqueles Spindola"
    assert customer.status == CustomerStatus.ACTIVE
    assert customer.id is not None


def test_customer_requires_business_name():
    with pytest.raises(ValueError):
        Customer("")

def test_customer_can_be_renamed():
    customer = Customer("Troqueles Spindola")

    customer.rename("Troqueles Spindola SA de CV")

    assert customer.business_name == "Troqueles Spindola SA de CV"


def test_customer_cannot_be_renamed_with_empty_name():
    customer = Customer("Troqueles Spindola")

    with pytest.raises(ValueError):
        customer.rename("")


def test_customer_can_be_deactivated():
    customer = Customer("Troqueles Spindola")

    customer.deactivate()

    assert customer.status == CustomerStatus.INACTIVE


def test_customer_can_be_reactivated():
    customer = Customer(
        "Troqueles Spindola",
        status=CustomerStatus.INACTIVE,
    )

    customer.reactivate()

    assert customer.status == CustomerStatus.ACTIVE