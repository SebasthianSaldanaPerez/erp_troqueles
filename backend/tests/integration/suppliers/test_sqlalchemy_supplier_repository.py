from src.infrastructure.database.models.supplier_model import SupplierModel
from src.infrastructure.database.session import SessionLocal
from src.shared.domain.value_objects.address import Address
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.value_objects.rfc import RFC
from src.suppliers.domain.supplier import Supplier
from src.suppliers.infrastructure.sqlalchemy_supplier_repository import (
    SQLAlchemySupplierRepository,
)


def test_sqlalchemy_supplier_repository_saves_and_gets_supplier():
    session = SessionLocal()

    try:
        repository = SQLAlchemySupplierRepository(session)

        supplier = Supplier(
            name="Aceros Industriales",
            email=Email("ventas@aceros.com"),
            rfc=RFC("ABC010203XYZ"),
            phone=Phone("4491234567"),
            address=Address(
                street="Av. Industria",
                exterior_number="100",
                city="Aguascalientes",
                state="Aguascalientes",
                postal_code="20000",
                country="Mexico",
            ),
            contact_name="Carlos Perez",
            notes="Integration test supplier",
        )

        repository.save(supplier)
        session.commit()

        saved_supplier = repository.get_by_id(supplier.id)

        assert saved_supplier is not None
        assert saved_supplier.id == supplier.id
        assert saved_supplier.name == "Aceros Industriales"

        assert saved_supplier.email is not None
        assert saved_supplier.email.value == "ventas@aceros.com"

        assert saved_supplier.rfc is not None
        assert saved_supplier.rfc.value == "ABC010203XYZ"

        assert saved_supplier.phone is not None
        assert saved_supplier.phone.value == "4491234567"

        assert saved_supplier.address is not None
        assert saved_supplier.address.street == "Av. Industria"
        assert saved_supplier.address.city == "Aguascalientes"

        assert saved_supplier.contact_name == "Carlos Perez"

    finally:
        if "supplier" in locals():
            model = session.get(
                SupplierModel,
                supplier.id,
            )

            if model is not None:
                session.delete(model)
                session.commit()

        session.close()