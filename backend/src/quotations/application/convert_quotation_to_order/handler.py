from uuid import UUID

from src.orders.domain.order import Order
from src.orders.domain.order_item import OrderItem
from src.orders.domain.order_repository import OrderRepository
from src.orders.domain.order_revision import OrderRevision
from src.orders.domain.order_revision_repository import (
    OrderRevisionRepository,
)

from src.quotations.application.errors import (
    QuotationNotFoundError,
    QuotationAlreadyConvertedError,
)
from src.quotations.domain.quotation import QuotationStatus
from src.quotations.domain.quotation_repository import (
    QuotationRepository,
)

from .command import ConvertQuotationToOrderCommand


class ConvertQuotationToOrderHandler:

    def __init__(
        self,
        quotation_repository: QuotationRepository,
        order_repository: OrderRepository,
        revision_repository: OrderRevisionRepository,
    ):
        self._quotation_repository = quotation_repository
        self._order_repository = order_repository
        self._revision_repository = revision_repository

    def execute(
        self,
        command: ConvertQuotationToOrderCommand,
    ) -> UUID:

        quotation = self._quotation_repository.get_by_id(
            command.quotation_id
        )

        if quotation is None:
            raise QuotationNotFoundError(
                f"Quotation {command.quotation_id} was not found"
            )

        if quotation.status != QuotationStatus.ACCEPTED:
            raise ValueError(
                "Only accepted quotations can be converted to orders"
            )

        existing_order = (
            self._order_repository.get_by_origin_quotation_id(
                quotation.id
            )
        )

        if existing_order is not None:
            raise QuotationAlreadyConvertedError(
                "This quotation has already been converted to an order"
            )

        order = Order(
            customer_id=quotation.customer_id,
            origin_quotation_id=quotation.id,
            tax_rate=quotation.tax_rate,
            currency=quotation.currency,
        )

        for quotation_item in quotation.items:
            order_item = OrderItem(
                description=quotation_item.description,
                quantity=quotation_item.quantity,
                unit_price=quotation_item.unit_price,
            )

            order.add_item(order_item)

        initial_revision = OrderRevision.create_initial(
            order_id=order.id,
            snapshot=order.snapshot(),
            created_by=command.user_id,
        )

        self._order_repository.save(order)
        self._revision_repository.save(initial_revision)

        return order.id