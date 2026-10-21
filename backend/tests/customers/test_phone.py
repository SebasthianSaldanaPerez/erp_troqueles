import pytest

from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.errors import InvalidPhoneError


def test_phone_is_created():
    phone = Phone("4491234567")

    assert phone.value == "4491234567"


def test_phone_is_normalized():
    phone = Phone("(449) 123-4567")

    assert phone.value == "4491234567"


def test_phone_cannot_be_empty():
    with pytest.raises(InvalidPhoneError):
        Phone("")


def test_phone_must_have_valid_length():
    with pytest.raises(InvalidPhoneError):
        Phone("123")