from decimal import Decimal
from uuid import uuid4

from src.infrastructure.database.models.quotation_model import QuotationModel
from src.infrastructure.database.session import SessionLocal
from src.quotations.domain.quotation import Quotation, QuotationStatus
from src.quotations.domain.quotation_item import QuotationItem
from src.quotations.infrastructure.sqlalchemy_quotation_repository import (
    SQLAlchemyQuotationRepository,
)
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate
from src.customers.domain.customer import Customer
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.models.customer_model import CustomerModel


def test_sqlalchemy_quotation_repository_saves_and_gets_quotation_with_items():
    session = SessionLocal()

    try:
        repository = SQLAlchemyQuotationRepository(session)
        customer_repository = SQLAlchemyCustomerRepository(session)

        customer = Customer(
            business_name="Quotation Integration Customer",
        )

        customer_repository.save(customer)
        session.commit()

        quotation = Quotation(
        customer_id=customer.id,
        tax_rate=TaxRate(Decimal("16")),
        currency="MXN",
        )

        quotation.add_item(
            QuotationItem(
                description="Troquel industrial",
                quantity=2,
                unit_price=Money(
                    Decimal("1500.00"),
                    "MXN",
                ),
            )
        )

        quotation.add_item(
            QuotationItem(
                description="Ajuste adicional",
                quantity=1,
                unit_price=Money(
                    Decimal("500.00"),
                    "MXN",
                ),
            )
        )

        repository.save(quotation)
        session.commit()

        saved_quotation = repository.get_by_id(quotation.id)

        assert saved_quotation is not None
        assert saved_quotation.id == quotation.id
        assert saved_quotation.customer_id == quotation.customer_id
        assert saved_quotation.status == QuotationStatus.DRAFT
        assert saved_quotation.tax_rate.value == Decimal("16.00")
        assert saved_quotation.currency == "MXN"

        assert len(saved_quotation.items) == 2

        assert saved_quotation.items[0].description == "Troquel industrial"
        assert saved_quotation.items[0].quantity == 2
        assert saved_quotation.items[0].unit_price.amount == Decimal("1500.00")

        assert saved_quotation.items[1].description == "Ajuste adicional"
        assert saved_quotation.items[1].quantity == 1
        assert saved_quotation.items[1].unit_price.amount == Decimal("500.00")

        assert saved_quotation.subtotal.amount == Decimal("3500.00")
        assert saved_quotation.tax.amount == Decimal("560.00")
        assert saved_quotation.total.amount == Decimal("4060.00")

    finally:
        if "quotation" in locals():
            quotation_model = session.get(
                QuotationModel,
                quotation.id,
            )

            if quotation_model is not None:
                session.delete(quotation_model)
                session.commit()

        if "customer" in locals():
            customer_model = session.get(
                CustomerModel,
                customer.id,
            )

            if customer_model is not None:
                session.delete(customer_model)
                session.commit()

        session.close()
        
def test_sqlalchemy_quotation_repository_rehydrates_sent_quotation():
    session = SessionLocal()

    try:
        customer_repository = SQLAlchemyCustomerRepository(session)
        quotation_repository = SQLAlchemyQuotationRepository(session)

        customer = Customer(
            business_name="Sent Quotation Customer",
        )

        customer_repository.save(customer)
        session.commit()

        quotation = Quotation(
            customer_id=customer.id,
            tax_rate=TaxRate(Decimal("16")),
            currency="MXN",
        )

        quotation.add_item(
            QuotationItem(
                description="Troquel industrial",
                quantity=1,
                unit_price=Money(
                    Decimal("1000.00"),
                    "MXN",
                ),
            )
        )

        quotation.send()

        quotation_repository.save(quotation)
        session.commit()

        saved_quotation = quotation_repository.get_by_id(
            quotation.id
        )

        assert saved_quotation is not None
        assert saved_quotation.status == QuotationStatus.SENT
        assert len(saved_quotation.items) == 1

    finally:
        if "quotation" in locals():
            quotation_model = session.get(
                QuotationModel,
                quotation.id,
            )

            if quotation_model is not None:
                session.delete(quotation_model)
                session.commit()

        if "customer" in locals():
            customer_model = session.get(
                CustomerModel,
                customer.id,
            )

            if customer_model is not None:
                session.delete(customer_model)
                session.commit()

        session.close()