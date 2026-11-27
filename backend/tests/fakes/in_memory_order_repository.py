from uuid import UUID

from src.orders.domain.order import Order
from src.orders.domain.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self.orders = []

    def save(self, order: Order) -> None:
        for index, existing_order in enumerate(self.orders):
            if existing_order.id == order.id:
                self.orders[index] = order
                return

        self.orders.append(order)

    def get_by_id(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                return order

        return None

    def get_by_origin_quotation_id(
        self,
        quotation_id: UUID,
    ) -> Order | None:
        return next(
            (
                order
                for order in self._orders.values()
                if order.origin_quotation_id == quotation_id
            ),
            None,
        )

    def list_all(self) -> list[Order]:
        return list(self.orders)