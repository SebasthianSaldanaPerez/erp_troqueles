from src.documents.domain.document import Document
from src.documents.domain.document_repository import DocumentRepository

from .query import ListDocumentsByOrderQuery


class ListDocumentsByOrderHandler:

    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListDocumentsByOrderQuery,
    ) -> list[Document]:
        return self._repository.list_by_order_id(
            query.order_id
        )