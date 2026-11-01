from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.invoices.application.register_invoice.command import (
    RegisterInvoiceCommand,
)
from src.invoices.application.register_invoice.handler import (
    RegisterInvoiceHandler,
)
from src.invoices.infrastructure.sqlalchemy_invoice_repository import (
    SQLAlchemyInvoiceRepository,
)
from src.orders.application.errors import OrderNotFoundError
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.presentation.api.dependencies import (
    get_db,
    get_invoice_repository,
    get_order_repository,
)
from src.presentation.api.invoices.schemas import (
    RegisterInvoiceRequest,
    RegisterInvoiceResponse,
)
from src.invoices.application.list_invoices_by_order.handler import (
    ListInvoicesByOrderHandler,
)
from src.invoices.application.list_invoices_by_order.query import (
    ListInvoicesByOrderQuery,
)
from src.presentation.api.invoices.mappers import invoice_to_response
from src.presentation.api.invoices.schemas import InvoiceResponse


router = APIRouter(
    tags=["Invoices"],
)


@router.post(
    "/orders/{order_id}/invoices",
    response_model=RegisterInvoiceResponse,
    status_code=201,
)
def register_invoice(
    order_id: UUID,
    request: RegisterInvoiceRequest,
    db: Session = Depends(get_db),
    invoice_repository: SQLAlchemyInvoiceRepository = Depends(
        get_invoice_repository
    ),
    order_repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> RegisterInvoiceResponse:
    handler = RegisterInvoiceHandler(
        invoice_repository=invoice_repository,
        order_repository=order_repository,
    )

    try:
        invoice_id = handler.execute(
            RegisterInvoiceCommand(
                order_id=order_id,
                folio=request.folio,
                invoice_date=request.invoice_date,
                total=request.total,
                currency=request.currency,
            )
        )

        db.commit()

    except OrderNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Order not found",
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

    return RegisterInvoiceResponse(
        id=str(invoice_id),
    )

@router.get(
    "/orders/{order_id}/invoices",
    response_model=list[InvoiceResponse],
)
def list_invoices_by_order(
    order_id: UUID,
    repository: SQLAlchemyInvoiceRepository = Depends(
        get_invoice_repository
    ),
) -> list[InvoiceResponse]:
    handler = ListInvoicesByOrderHandler(repository)

    invoices = handler.execute(
        ListInvoicesByOrderQuery(
            order_id=order_id,
        )
    )

    return [
        invoice_to_response(invoice)
        for invoice in invoices
    ]