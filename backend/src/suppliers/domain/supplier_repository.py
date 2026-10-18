from abc import ABC, abstractmethod
from uuid import UUID

from .supplier import Supplier


class SupplierRepository(ABC):

    @abstractmethod
    def save(self, supplier: Supplier) -> None:
        pass

    @abstractmethod
    def get_by_id(self, supplier_id: UUID) -> Supplier | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Supplier]:
        pass