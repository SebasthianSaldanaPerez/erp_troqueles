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