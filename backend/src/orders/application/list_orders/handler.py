from src.orders.domain.order import Order
from src.orders.domain.order_repository import OrderRepository

from .query import ListOrdersQuery


class ListOrdersHandler:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(
        self,
        query: ListOrdersQuery,
    ) -> list[Order]:
        return self._repository.list_all()