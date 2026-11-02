from src.documents.domain.document import Document
from src.presentation.api.documents.schemas import DocumentResponse


def document_to_response(
    document: Document,
) -> DocumentResponse:
    return DocumentResponse(
        id=str(document.id),
        order_id=str(document.order_id),
        filename=document.filename,
        mime_type=document.mime_type,
        size=document.size,
        document_type=document.document_type.value,
        uploaded_by=str(document.uploaded_by),
        status=document.status.value,
    )