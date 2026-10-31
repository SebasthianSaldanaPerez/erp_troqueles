from uuid import uuid4

import pytest

from src.documents.domain.document import (
    Document,
    DocumentStatus,
    DocumentType,
)


def test_document_is_created():
    document = Document(
        filename="invoice.pdf",
        object_key="orders/ORD-001/invoice.pdf",
        mime_type="application/pdf",
        size=1024,
        document_type=DocumentType.INVOICE,
        uploaded_by=uuid4(),
    )

    assert document.id is not None
    assert document.filename == "invoice.pdf"
    assert document.object_key == "orders/ORD-001/invoice.pdf"
    assert document.size == 1024
    assert document.status == DocumentStatus.ACTIVE


def test_document_requires_filename():
    with pytest.raises(ValueError):
        Document(
            filename="",
            object_key="orders/file.pdf",
            mime_type="application/pdf",
            size=1024,
            document_type=DocumentType.OTHER,
            uploaded_by=uuid4(),
        )


def test_document_requires_object_key():
    with pytest.raises(ValueError):
        Document(
            filename="file.pdf",
            object_key="",
            mime_type="application/pdf",
            size=1024,
            document_type=DocumentType.OTHER,
            uploaded_by=uuid4(),
        )


def test_document_size_cannot_be_negative():
    with pytest.raises(ValueError):
        Document(
            filename="file.pdf",
            object_key="orders/file.pdf",
            mime_type="application/pdf",
            size=-1,
            document_type=DocumentType.OTHER,
            uploaded_by=uuid4(),
        )


def test_document_can_be_archived():
    document = Document(
        filename="file.pdf",
        object_key="orders/file.pdf",
        mime_type="application/pdf",
        size=1024,
        document_type=DocumentType.OTHER,
        uploaded_by=uuid4(),
    )

    document.archive()

    assert document.status == DocumentStatus.ARCHIVED


def test_archived_document_cannot_be_archived_again():
    document = Document(
        filename="file.pdf",
        object_key="orders/file.pdf",
        mime_type="application/pdf",
        size=1024,
        document_type=DocumentType.OTHER,
        uploaded_by=uuid4(),
    )

    document.archive()

    with pytest.raises(ValueError):
        document.archive()