from abc import ABC, abstractmethod
from uuid import UUID

from .order_revision import OrderRevision


class OrderRevisionRepository(ABC):

    @abstractmethod
    def save(self, revision: OrderRevision) -> None:
        pass

    @abstractmethod
    def list_by_order_id(self, order_id: UUID) -> list[OrderRevision]:
        pass