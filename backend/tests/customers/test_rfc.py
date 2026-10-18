import pytest

from src.shared.domain.value_object.rfc import RFC
from src.shared.domain.errors import InvalidRFCError

def test_rfc_is_created():
    rfc = RFC("ABC010203XYZ")

    assert rfc.value == "ABC010203XYZ"


def test_rfc_is_normalized():
    rfc = RFC("  abc010203xyz  ")

    assert rfc.value == "ABC010203XYZ"


def test_rfc_cannot_be_empty():
    with pytest.raises(InvalidRFCError):
        RFC("")


def test_rfc_must_have_valid_format():
    with pytest.raises(InvalidRFCError):
        RFC("INVALID")