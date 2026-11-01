from uuid import UUID

from pathlib import Path

from fastapi.responses import FileResponse

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from src.documents.application import file_storage
from src.documents.application.upload_order_document.command import (
    UploadOrderDocumentCommand,
)
from src.documents.application.archive_document.command import (
    ArchiveDocumentCommand,
)
from src.documents.application.archive_document.handler import (
    ArchiveDocumentHandler,
)
from src.documents.application.upload_order_document.handler import (
    UploadOrderDocumentHandler,
)
from src.documents.domain.document import DocumentType
from src.orders.application.errors import OrderNotFoundError
from src.presentation.api.dependencies import (
    get_db,
    get_document_repository,
    get_file_storage,
    get_order_repository,
)
from src.documents.application.errors import DocumentNotFoundError
from src.presentation.api.documents.mappers import document_to_response
from src.presentation.api.documents.schemas import DocumentResponse


router = APIRouter(
    tags=["Documents"],
)


@router.post(
    "/orders/{order_id}/documents",
    status_code=201,
)
async def upload_order_document(
    order_id: UUID,
    document_type: DocumentType = Form(...),
    uploaded_by: UUID = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    order_repository=Depends(get_order_repository),
    document_repository=Depends(get_document_repository),
    file_storage=Depends(get_file_storage),
):
    handler = UploadOrderDocumentHandler(
        order_repository=order_repository,
        document_repository=document_repository,
        file_storage=file_storage,
    )

    content = await file.read()

    try:
        document_id = handler.execute(
            UploadOrderDocumentCommand(
                order_id=order_id,
                filename=file.filename or "file",
                content=content,
                mime_type=file.content_type or "application/octet-stream",
                document_type=document_type,
                uploaded_by=uploaded_by,
            )
        )

        db.commit()

    except OrderNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Order not found",
        ) from error

    except Exception:
        db.rollback()
        raise

    return {
        "id": str(document_id),
    }

@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    document_repository=Depends(get_document_repository),
) -> DocumentResponse:
    document = document_repository.get_by_id(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return document_to_response(document)



@router.get(
    "/documents/{document_id}/download",
)
def download_document(
    document_id: UUID,
    document_repository=Depends(get_document_repository),
    file_storage=Depends(get_file_storage),
):
    document = document_repository.get_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    path = file_storage.get_path(document.object_key)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="Stored file not found",
        )

    return FileResponse(
        path=path,
        media_type=document.mime_type,
        filename=document.filename,
        content_disposition_type="inline",
    )

@router.patch(
    "/documents/{document_id}/archive",
    status_code=204,
)
def archive_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    repository=Depends(get_document_repository),
) -> None:
    handler = ArchiveDocumentHandler(repository)

    try:
        handler.execute(
            ArchiveDocumentCommand(
                document_id=document_id,
            )
        )

        db.commit()

    except DocumentNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        ) from error

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise