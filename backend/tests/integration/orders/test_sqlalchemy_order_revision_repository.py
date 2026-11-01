from decimal import Decimal
from uuid import uuid4

from src.shared.domain.value_objects.tax_rate import TaxRate
from src.customers.domain.customer import Customer
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.models.customer_model import CustomerModel
from src.infrastructure.database.models.order_model import OrderModel
from src.infrastructure.database.session import SessionLocal
from src.orders.domain.order import Order
from src.orders.domain.order_revision import OrderRevision
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.orders.infrastructure.sqlalchemy_order_revision_repository import (
    SQLAlchemyOrderRevisionRepository,
)
from src.infrastructure.database.models.order_revision_model import (
    OrderRevisionModel,
)


def test_sqlalchemy_order_revision_repository_saves_and_lists_revisions():
    session = SessionLocal()

    try:
        customer_repository = SQLAlchemyCustomerRepository(session)
        order_repository = SQLAlchemyOrderRepository(session)
        revision_repository = SQLAlchemyOrderRevisionRepository(session)

        customer = Customer(
            business_name="Revision Integration Customer",
        )

        customer_repository.save(customer)
        session.commit()

        order = Order(
            customer_id=customer.id,
            currency="MXN",
            tax_rate=TaxRate(Decimal("16"))
        )

        order_repository.save(order)
        session.commit()

        revision = OrderRevision.create(
            order_id=order.id,
            revision_number=1,
            snapshot={
                "status": "CREATED",
                "total": "1160.00",
            },
            reason="Customer requested changes",
            created_by=uuid4(),
        )

        revision_repository.save(revision)
        session.commit()

        revisions = revision_repository.list_by_order_id(
            order.id
        )

        assert len(revisions) == 1
        assert revisions[0].id == revision.id
        assert revisions[0].order_id == order.id
        assert revisions[0].revision_number == 1
        assert revisions[0].reason == "Customer requested changes"
        assert revisions[0].snapshot["total"] == "1160.00"

    finally:
        session.rollback()

        if "order" in locals():
            revisions = session.query(OrderRevisionModel).filter(
                OrderRevisionModel.order_id == order.id
            ).all()

            for revision_model in revisions:
                session.delete(revision_model)

            session.commit()

            order_model = session.get(
                OrderModel,
                order.id,
            )

            if order_model is not None:
                session.delete(order_model)
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