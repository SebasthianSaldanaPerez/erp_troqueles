from decimal import Decimal

from src.shared.domain.value_objects.tax_rate import TaxRate
from src.customers.domain.customer import Customer
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.models.customer_model import CustomerModel
from src.infrastructure.database.models.order_model import OrderModel
from src.infrastructure.database.session import SessionLocal
from src.orders.domain.order import (
    BillingStatus,
    Order,
    OrderStatus,
)
from src.orders.domain.order_item import OrderItem
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.shared.domain.value_objects.money import Money


def test_sqlalchemy_order_repository_saves_and_gets_order_with_items():
    session = SessionLocal()

    try:
        customer_repository = SQLAlchemyCustomerRepository(session)
        order_repository = SQLAlchemyOrderRepository(session)

        customer = Customer(
            business_name="Order Integration Customer",
        )

        customer_repository.save(customer)
        session.commit()

        order = Order(
            customer_id=customer.id,
            tax_rate=TaxRate(Decimal("16")),
            currency="MXN",
        )

        order.add_item(
            OrderItem(
                description="Troquel industrial",
                quantity=2,
                unit_price=Money(
                    Decimal("1500.00"),
                    "MXN",
                ),
            )
        )

        order.add_item(
            OrderItem(
                description="Ajuste adicional",
                quantity=1,
                unit_price=Money(
                    Decimal("500.00"),
                    "MXN",
                ),
            )
        )

        order_repository.save(order)
        session.commit()

        saved_order = order_repository.get_by_id(order.id)

        assert saved_order is not None
        assert saved_order.id == order.id
        assert saved_order.customer_id == customer.id
        assert saved_order.status == OrderStatus.CREATED
        assert saved_order.billing_status == BillingStatus.NOT_INVOICED
        assert saved_order.currency == "MXN"
        assert saved_order.revision_number == 0

        assert len(saved_order.items) == 2

        assert saved_order.items[0].description == "Troquel industrial"
        assert saved_order.items[0].quantity == 2
        assert saved_order.items[0].unit_price.amount == Decimal("1500.00")

        assert saved_order.items[1].description == "Ajuste adicional"
        assert saved_order.items[1].quantity == 1
        assert saved_order.items[1].unit_price.amount == Decimal("500.00")

        assert saved_order.total.amount == Decimal("4060.00")

    finally:
        session.rollback()

        if "order" in locals():
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

def test_sqlalchemy_order_repository_rehydrates_delivered_order():
    session = SessionLocal()

    try:
        customer_repository = SQLAlchemyCustomerRepository(session)
        order_repository = SQLAlchemyOrderRepository(session)

        customer = Customer(
            business_name="Delivered Order Customer",
        )

        customer_repository.save(customer)
        session.commit()

        order = Order(
            customer_id=customer.id,
            currency="MXN",
            tax_rate=TaxRate(Decimal("16")),
        )

        order.add_item(
            OrderItem(
                description="Troquel terminado",
                quantity=1,
                unit_price=Money(
                    Decimal("5000.00"),
                    "MXN",
                ),
            )
        )

        order.start()
        order.deliver()

        order.update_billing_status(
            Money(
                Decimal("5800.00"),
                "MXN",
            )
        )

        order.increment_revision()

        order_repository.save(order)
        session.commit()

        saved_order = order_repository.get_by_id(order.id)

        assert saved_order is not None
        assert saved_order.status == OrderStatus.DELIVERED
        assert saved_order.billing_status == BillingStatus.FULLY_INVOICED
        assert saved_order.revision_number == 1
        assert len(saved_order.items) == 1
        assert saved_order.items[0].description == "Troquel terminado"

    finally:
        session.rollback()

        if "order" in locals():
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