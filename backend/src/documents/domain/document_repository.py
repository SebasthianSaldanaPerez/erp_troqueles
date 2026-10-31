from abc import ABC, abstractmethod
from uuid import UUID

from .document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document: Document) -> None:
        pass

    @abstractmethod
    def get_by_id(self, document_id: UUID) -> Document | None:
        pass