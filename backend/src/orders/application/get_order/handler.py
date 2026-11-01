from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order import Order
from src.orders.domain.order_repository import OrderRepository

from .query import GetOrderQuery


class GetOrderHandler:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, query: GetOrderQuery) -> Order:
        order = self._repository.get_by_id(query.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {query.order_id} was not found"
            )

        return order