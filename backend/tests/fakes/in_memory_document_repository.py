from src.documents.domain.document import Document
from src.documents.domain.document_repository import DocumentRepository


class InMemoryDocumentRepository(DocumentRepository):

    def __init__(self):
        self.documents = []

    def save(self, document: Document) -> None:
        for index, existing_document in enumerate(self.documents):
            if existing_document.id == document.id:
                self.documents[index] = document
                return

        self.documents.append(document)

    def get_by_id(self, document_id):
        for document in self.documents:
            if document.id == document_id:
                return document

        return None