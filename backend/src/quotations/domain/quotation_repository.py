from abc import ABC, abstractmethod
from uuid import UUID

from .quotation import Quotation


class QuotationRepository(ABC):

    @abstractmethod
    def save(self, quotation: Quotation) -> None:
        pass

    @abstractmethod
    def get_by_id(self, quotation_id: UUID) -> Quotation | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Quotation]:
        pass