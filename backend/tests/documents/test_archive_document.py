from uuid import uuid4

import pytest

from src.documents.application.archive_document.command import (
    ArchiveDocumentCommand,
)
from src.documents.application.archive_document.handler import (
    ArchiveDocumentHandler,
)
from src.documents.application.errors import DocumentNotFoundError
from src.documents.domain.document import (
    Document,
    DocumentStatus,
    DocumentType,
)
from tests.fakes.in_memory_document_repository import (
    InMemoryDocumentRepository,
)


def create_document() -> Document:
    return Document(
        filename="invoice.pdf",
        object_key="orders/ORD-001/invoice.pdf",
        mime_type="application/pdf",
        size=1024,
        document_type=DocumentType.INVOICE,
        uploaded_by=uuid4(),
    )


def test_archive_document():
    repository = InMemoryDocumentRepository()

    document = create_document()
    repository.save(document)

    handler = ArchiveDocumentHandler(repository)

    handler.execute(
        ArchiveDocumentCommand(
            document_id=document.id,
        )
    )

    saved_document = repository.get_by_id(document.id)

    assert saved_document is not None
    assert saved_document.status == DocumentStatus.ARCHIVED


def test_archived_document_cannot_be_archived_again():
    repository = InMemoryDocumentRepository()

    document = create_document()
    document.archive()
    repository.save(document)

    handler = ArchiveDocumentHandler(repository)

    with pytest.raises(ValueError):
        handler.execute(
            ArchiveDocumentCommand(
                document_id=document.id,
            )
        )


def test_archive_document_raises_error_when_document_does_not_exist():
    repository = InMemoryDocumentRepository()

    handler = ArchiveDocumentHandler(repository)

    with pytest.raises(DocumentNotFoundError):
        handler.execute(
            ArchiveDocumentCommand(
                document_id=uuid4(),
            )
        )