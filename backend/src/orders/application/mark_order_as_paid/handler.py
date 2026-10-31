from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository

from .command import MarkOrderAsPaidCommand


class MarkOrderAsPaidHandler:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, command: MarkOrderAsPaidCommand) -> None:
        order = self._repository.get_by_id(command.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {command.order_id} was not found"
            )

        order.mark_as_paid()

        self._repository.save(order)