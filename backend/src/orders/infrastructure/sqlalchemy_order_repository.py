from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.infrastructure.database.models.order_model import (
    OrderItemModel,
    OrderModel,
)
from src.orders.domain.order import (
    BillingStatus,
    Order,
    OrderStatus,
)
from src.orders.domain.order_item import OrderItem
from src.orders.domain.order_repository import OrderRepository
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate


class SQLAlchemyOrderRepository(OrderRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, order: Order) -> None:
        model = self._session.get(
            OrderModel,
            order.id,
        )

        if model is None:
            model = OrderModel(
                id=order.id,
                customer_id=order.customer_id,
                origin_quotation_id=order.origin_quotation_id,
                status=order.status.value,
                billing_status=order.billing_status.value,
                tax_rate=order.tax_rate.value,
                currency=order.currency,
                revision_number=order.revision_number,
            )

            model.items = [
                self._item_to_model(
                    order_id=order.id,
                    item=item,
                )
                for item in order.items
            ]

            self._session.add(model)
            return

        model.customer_id = order.customer_id
        model.origin_quotation_id = order.origin_quotation_id
        model.status = order.status.value
        model.billing_status = order.billing_status.value
        model.currency = order.currency
        model.tax_rate = order.tax_rate.value
        model.revision_number = order.revision_number

        model.items = [
            self._item_to_model(
                order_id=order.id,
                item=item,
            )
            for item in order.items
        ]

    def get_by_id(
        self,
        order_id: UUID,
    ) -> Order | None:
        statement = (
            select(OrderModel)
            .options(
                selectinload(OrderModel.items)
            )
            .where(OrderModel.id == order_id)
        )

        model = self._session.scalars(
            statement
        ).first()

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[Order]:
        statement = (
            select(OrderModel)
            .options(
                selectinload(OrderModel.items)
            )
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _item_to_model(
        order_id: UUID,
        item: OrderItem,
    ) -> OrderItemModel:
        return OrderItemModel(
            id=item.id,
            order_id=order_id,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price.amount,
            currency=item.unit_price.currency,
        )

    @staticmethod
    def _to_domain(
        model: OrderModel,
    ) -> Order:
        items = [
            OrderItem(
                item_id=item_model.id,
                description=item_model.description,
                quantity=item_model.quantity,
                unit_price=Money(
                    amount=item_model.unit_price,
                    currency=item_model.currency,
                ),
            )
            for item_model in model.items
        ]

        return Order.rehydrate(
            order_id=model.id,
            customer_id=model.customer_id,
            origin_quotation_id=model.origin_quotation_id,
            tax_rate=TaxRate(model.tax_rate),
            currency=model.currency,
            status=OrderStatus(model.status),
            billing_status=BillingStatus(model.billing_status),
            revision_number=model.revision_number,
            items=items,
        )