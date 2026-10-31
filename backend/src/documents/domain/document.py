from enum import Enum
from uuid import UUID, uuid4


class DocumentStatus(Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class DocumentType(Enum):
    QUOTATION = "QUOTATION"
    INVOICE = "INVOICE"
    EXPENSE_RECEIPT = "EXPENSE_RECEIPT"
    TECHNICAL_DRAWING = "TECHNICAL_DRAWING"
    ORDER_ATTACHMENT = "ORDER_ATTACHMENT"
    IMAGE = "IMAGE"
    OTHER = "OTHER"


class Document:
    def __init__(
        self,
        filename: str,
        object_key: str,
        mime_type: str,
        size: int,
        document_type: DocumentType,
        uploaded_by: UUID,
        document_id: UUID | None = None,
        status: DocumentStatus = DocumentStatus.ACTIVE,
    ):
        self._id = document_id or uuid4()
        self._filename = self._validate_filename(filename)
        self._object_key = self._validate_object_key(object_key)
        self._mime_type = mime_type.strip()
        self._size = self._validate_size(size)
        self._document_type = document_type
        self._uploaded_by = uploaded_by
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def object_key(self) -> str:
        return self._object_key

    @property
    def mime_type(self) -> str:
        return self._mime_type

    @property
    def size(self) -> int:
        return self._size

    @property
    def document_type(self) -> DocumentType:
        return self._document_type

    @property
    def uploaded_by(self) -> UUID:
        return self._uploaded_by

    @property
    def status(self) -> DocumentStatus:
        return self._status

    def archive(self) -> None:
        if self._status == DocumentStatus.ARCHIVED:
            raise ValueError("Document is already archived")

        self._status = DocumentStatus.ARCHIVED

    @staticmethod
    def _validate_filename(filename: str) -> str:
        if not filename or not filename.strip():
            raise ValueError("Filename is required")

        return filename.strip()

    @staticmethod
    def _validate_object_key(object_key: str) -> str:
        if not object_key or not object_key.strip():
            raise ValueError("Object key is required")

        return object_key.strip()

    @staticmethod
    def _validate_size(size: int) -> int:
        if size < 0:
            raise ValueError("Document size cannot be negative")

        return size