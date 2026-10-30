from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository

from .command import CancelOrderCommand


class CancelOrderHandler:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, command: CancelOrderCommand) -> None:
        order = self._repository.get_by_id(command.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {command.order_id} was not found"
            )

        order.cancel()

        self._repository.save(order)