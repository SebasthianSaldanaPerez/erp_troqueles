from abc import ABC, abstractmethod
from uuid import UUID

from .invoice import Invoice


class InvoiceRepository(ABC):

    @abstractmethod
    def save(self, invoice: Invoice) -> None:
        pass

    @abstractmethod
    def get_by_id(self, invoice_id: UUID) -> Invoice | None:
        pass

    @abstractmethod
    def list_by_order_id(self, order_id: UUID) -> list[Invoice]:
        pass