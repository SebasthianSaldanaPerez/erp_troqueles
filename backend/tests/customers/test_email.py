import pytest

from src.customers.domain.value_objects.email import Email


def test_email_is_created():
    email = Email("ventas@empresa.com")

    assert email.value == "ventas@empresa.com"


def test_email_is_normalized():
    email = Email("  VENTAS@EMPRESA.COM  ")

    assert email.value == "ventas@empresa.com"


def test_email_cannot_be_empty():
    with pytest.raises(ValueError):
        Email("")


def test_email_must_have_valid_format():
    with pytest.raises(ValueError):
        Email("this-is-not-an-email")