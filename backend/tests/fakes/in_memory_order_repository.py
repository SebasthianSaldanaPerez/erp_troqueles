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