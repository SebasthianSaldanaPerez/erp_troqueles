import pytest

from src.suppliers.domain.supplier import Supplier, SupplierStatus


def test_supplier_is_created_active():
    supplier = Supplier("Aceros Industriales")

    assert supplier.name == "Aceros Industriales"
    assert supplier.status == SupplierStatus.ACTIVE
    assert supplier.id is not None


def test_supplier_requires_name():
    with pytest.raises(ValueError):
        Supplier("")


def test_supplier_can_be_renamed():
    supplier = Supplier("Aceros Industriales")

    supplier.rename("Aceros Industriales SA de CV")

    assert supplier.name == "Aceros Industriales SA de CV"


def test_supplier_can_be_deactivated():
    supplier = Supplier("Aceros Industriales")

    supplier.deactivate()

    assert supplier.status == SupplierStatus.INACTIVE


def test_supplier_can_be_reactivated():
    supplier = Supplier(
        "Aceros Industriales",
        status=SupplierStatus.INACTIVE,
    )

    supplier.reactivate()

    assert supplier.status == SupplierStatus.ACTIVE