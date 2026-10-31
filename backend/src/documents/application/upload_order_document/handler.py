from uuid import UUID, uuid4

from src.documents.application.file_storage import FileStorage
from src.documents.domain.document import Document
from src.documents.domain.document_repository import DocumentRepository
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository

from .command import UploadOrderDocumentCommand


class UploadOrderDocumentHandler:

    def __init__(
        self,
        order_repository: OrderRepository,
        document_repository: DocumentRepository,
        file_storage: FileStorage,
    ):
        self._order_repository = order_repository
        self._document_repository = document_repository
        self._file_storage = file_storage

    def execute(self, command: UploadOrderDocumentCommand) -> UUID:
        order = self._order_repository.get_by_id(command.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {command.order_id} was not found"
            )

        document_id = uuid4()

        object_key = (
            f"orders/{command.order_id}/"
            f"{document_id}-{command.filename}"
        )

        self._file_storage.upload(
            object_key=object_key,
            content=command.content,
            content_type=command.mime_type,
        )

        document = Document(
            document_id=document_id,
            filename=command.filename,
            object_key=object_key,
            mime_type=command.mime_type,
            size=len(command.content),
            document_type=command.document_type,
            uploaded_by=command.uploaded_by,
        )

        self._document_repository.save(document)

        return document.id