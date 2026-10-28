from uuid import UUID

from src.orders.domain.order import Order
from src.orders.domain.order_item import OrderItem
from src.orders.domain.order_repository import OrderRepository
from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation import QuotationStatus
from src.quotations.domain.quotation_repository import QuotationRepository

from .command import ConvertQuotationToOrderCommand


class ConvertQuotationToOrderHandler:

    def __init__(
        self,
        quotation_repository: QuotationRepository,
        order_repository: OrderRepository,
    ):
        self._quotation_repository = quotation_repository
        self._order_repository = order_repository

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

        order = Order(
            customer_id=quotation.customer_id,
            origin_quotation_id=quotation.id,
            currency=quotation.total.currency,
        )

        for quotation_item in quotation.items:
            order_item = OrderItem(
                description=quotation_item.description,
                quantity=quotation_item.quantity,
                unit_price=quotation_item.unit_price,
            )

            order.add_item(order_item)

        self._order_repository.save(order)

        return order.id