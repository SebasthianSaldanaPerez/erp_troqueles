from uuid import uuid4

import pytest

from src.documents.application.upload_order_document.command import (
    UploadOrderDocumentCommand,
)
from src.documents.application.upload_order_document.handler import (
    UploadOrderDocumentHandler,
)
from src.documents.domain.document import DocumentType
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order import Order
from tests.fakes.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from tests.fakes.in_memory_file_storage import InMemoryFileStorage
from tests.fakes.in_memory_order_repository import InMemoryOrderRepository


def test_upload_order_document():
    order_repository = InMemoryOrderRepository()
    document_repository = InMemoryDocumentRepository()
    file_storage = InMemoryFileStorage()

    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )
    order_repository.save(order)

    handler = UploadOrderDocumentHandler(
        order_repository=order_repository,
        document_repository=document_repository,
        file_storage=file_storage,
    )

    content = b"fake pdf content"

    document_id = handler.execute(
        UploadOrderDocumentCommand(
            order_id=order.id,
            filename="drawing.pdf",
            content=content,
            mime_type="application/pdf",
            document_type=DocumentType.TECHNICAL_DRAWING,
            uploaded_by=uuid4(),
        )
    )

    document = document_repository.get_by_id(document_id)

    assert document is not None
    assert document.filename == "drawing.pdf"
    assert document.size == len(content)

    assert document.object_key in file_storage.files
    assert file_storage.files[document.object_key]["content"] == content


def test_upload_order_document_raises_error_when_order_does_not_exist():
    handler = UploadOrderDocumentHandler(
        order_repository=InMemoryOrderRepository(),
        document_repository=InMemoryDocumentRepository(),
        file_storage=InMemoryFileStorage(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(
            UploadOrderDocumentCommand(
                order_id=uuid4(),
                filename="drawing.pdf",
                content=b"fake content",
                mime_type="application/pdf",
                document_type=DocumentType.TECHNICAL_DRAWING,
                uploaded_by=uuid4(),
            )
        )