from src.documents.application.errors import DocumentNotFoundError
from src.documents.domain.document_repository import DocumentRepository

from .command import ArchiveDocumentCommand


class ArchiveDocumentHandler:

    def __init__(self, repository: DocumentRepository):
        self._repository = repository

    def execute(self, command: ArchiveDocumentCommand) -> None:
        document = self._repository.get_by_id(command.document_id)

        if document is None:
            raise DocumentNotFoundError(
                f"Document {command.document_id} was not found"
            )

        document.archive()

        self._repository.save(document)