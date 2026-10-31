from dataclasses import dataclass
from uuid import UUID

from src.documents.domain.document import DocumentType


@dataclass(frozen=True)
class UploadOrderDocumentCommand:
    order_id: UUID
    filename: str
    content: bytes
    mime_type: str
    document_type: DocumentType
    uploaded_by: UUID