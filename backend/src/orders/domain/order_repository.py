from abc import ABC, abstractmethod
from uuid import UUID

from .order import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order | None:
        pass