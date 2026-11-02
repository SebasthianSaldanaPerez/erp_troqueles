from pydantic import BaseModel


class UploadDocumentResponse(BaseModel):
    id: str


class DocumentResponse(BaseModel):
    id: str
    order_id: str
    filename: str
    mime_type: str
    size: int
    document_type: str
    uploaded_by: str
    status: str

