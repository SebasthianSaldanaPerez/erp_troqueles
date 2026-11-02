from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.documents.domain.document import (
    Document,
    DocumentStatus,
    DocumentType,
)
from src.documents.domain.document_repository import DocumentRepository
from src.infrastructure.database.models.document_model import DocumentModel


class SQLAlchemyDocumentRepository(DocumentRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, document: Document) -> None:
        model = self._session.get(
            DocumentModel,
            document.id,
        )

        if model is None:
            model = DocumentModel(
                id=document.id,
                order_id=document.order_id,
                filename=document.filename,
                object_key=document.object_key,
                mime_type=document.mime_type,
                size=document.size,
                document_type=document.document_type.value,
                uploaded_by=document.uploaded_by,
                status=document.status.value,
            )

            self._session.add(model)
            return

        model.filename = document.filename
        model.object_key = document.object_key
        model.mime_type = document.mime_type
        model.size = document.size
        model.document_type = document.document_type.value
        model.uploaded_by = document.uploaded_by
        model.status = document.status.value

    def get_by_id(
        self,
        document_id: UUID,
    ) -> Document | None:
        model = self._session.get(
            DocumentModel,
            document_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_order_id(
        self,
        order_id: UUID,
    ) -> list[Document]:
        statement = select(DocumentModel).where(
            DocumentModel.order_id == order_id
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: DocumentModel,
    ) -> Document:
        return Document(
            document_id=model.id,
            order_id=model.order_id,
            filename=model.filename,
            object_key=model.object_key,
            mime_type=model.mime_type,
            size=model.size,
            document_type=DocumentType(model.document_type),
            uploaded_by=model.uploaded_by,
            status=DocumentStatus(model.status),
        )