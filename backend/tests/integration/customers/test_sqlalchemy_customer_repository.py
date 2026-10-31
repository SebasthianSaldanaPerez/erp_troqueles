from src.customers.domain.customer import Customer
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.models.customer_model import CustomerModel
from src.infrastructure.database.session import SessionLocal
from src.shared.domain.value_objects.address import Address
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.value_objects.rfc import RFC


def test_sqlalchemy_customer_repository_saves_and_gets_customer():
    session = SessionLocal()

    try:
        repository = SQLAlchemyCustomerRepository(session)

        customer = Customer(
            business_name="Troqueles Spindola",
            email=Email("ventas@troqueles.com"),
            rfc=RFC("ABC010203XYZ"),
            phone=Phone("4491234567"),
            address=Address(
                street="Av. Universidad",
                exterior_number="123",
                city="Aguascalientes",
                state="Aguascalientes",
                postal_code="20000",
                country="Mexico",
            ),
            contact_name="Hector",
            notes="Integration test customer",
        )

        repository.save(customer)
        session.commit()

        saved_customer = repository.get_by_id(customer.id)

        assert saved_customer is not None
        assert saved_customer.id == customer.id
        assert saved_customer.business_name == "Troqueles Spindola"
        assert saved_customer.email is not None
        assert saved_customer.email.value == "ventas@troqueles.com"
        assert saved_customer.rfc is not None
        assert saved_customer.rfc.value == "ABC010203XYZ"
        assert saved_customer.phone is not None
        assert saved_customer.phone.value == "4491234567"
        assert saved_customer.address is not None
        assert saved_customer.address.street == "Av. Universidad"
        assert saved_customer.contact_name == "Hector"

    finally:
        if "customer" in locals():
            model = session.get(CustomerModel, customer.id)

            if model is not None:
                session.delete(model)
                session.commit()

        session.close()