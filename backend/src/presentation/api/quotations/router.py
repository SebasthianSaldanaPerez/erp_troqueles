from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.quotations.application.create_quotation.command import (
    CreateQuotationCommand,
)
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.quotations.application.convert_quotation_to_order.command import (
    ConvertQuotationToOrderCommand,
)
from src.quotations.application.convert_quotation_to_order.handler import (
    ConvertQuotationToOrderHandler,
)
from src.quotations.application.accept_quotation.command import (
    AcceptQuotationCommand,
)
from src.quotations.application.accept_quotation.handler import (
    AcceptQuotationHandler,
)
from src.quotations.application.cancel_quotation.command import (
    CancelQuotationCommand,
)
from src.quotations.application.cancel_quotation.handler import (
    CancelQuotationHandler,
)
from src.quotations.application.reject_quotation.command import (
    RejectQuotationCommand,
)
from src.quotations.application.reject_quotation.handler import (
    RejectQuotationHandler,
)
from src.quotations.application.send_quotation.command import (
    SendQuotationCommand,
)
from src.quotations.application.send_quotation.handler import (
    SendQuotationHandler,
)
from src.quotations.application.create_quotation.handler import (
    CreateQuotationHandler,
)
from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.application.get_quotation.handler import (
    GetQuotationHandler,
)
from src.quotations.application.get_quotation.query import (
    GetQuotationQuery,
)
from src.quotations.application.list_quotations.handler import (
    ListQuotationsHandler,
)
from src.quotations.application.list_quotations.query import (
    ListQuotationsQuery,
)
from src.quotations.infrastructure.sqlalchemy_quotation_repository import (
    SQLAlchemyQuotationRepository,
)
from src.presentation.api.dependencies import (
    get_db,
    get_quotation_repository,
    get_order_repository,
)
from src.presentation.api.quotations.mappers import (
    quotation_to_response,
)
from src.presentation.api.quotations.schemas import (
    AddQuotationItemRequest,
    CreateQuotationRequest,
    CreateQuotationResponse,
    QuotationItemCreatedResponse,
    QuotationResponse,
    UpdateQuotationItemRequest,
    ConvertQuotationToOrderResponse,
)

from src.quotations.application.add_quotation_item.command import (
    AddQuotationItemCommand,
)
from src.quotations.application.add_quotation_item.handler import (
    AddQuotationItemHandler,
)
from src.quotations.application.remove_quotation_item.command import (
    RemoveQuotationItemCommand,
)
from src.quotations.application.remove_quotation_item.handler import (
    RemoveQuotationItemHandler,
)
from src.quotations.application.update_quotation_item.command import (
    UpdateQuotationItemCommand,
)
from src.quotations.application.update_quotation_item.handler import (
    UpdateQuotationItemHandler,
)

router = APIRouter(
    prefix="/quotations",
    tags=["Quotations"],
)

@router.post(
    "",
    response_model=CreateQuotationResponse,
    status_code=201,
)
def create_quotation(
    request: CreateQuotationRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> CreateQuotationResponse:
    handler = CreateQuotationHandler(repository)

    command = CreateQuotationCommand(
        customer_id=UUID(request.customer_id),
        tax_rate=request.tax_rate,
        currency=request.currency,
    )

    try:
        quotation_id = handler.execute(command)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return CreateQuotationResponse(
        id=str(quotation_id),
    )

@router.get(
    "",
    response_model=list[QuotationResponse],
)
def list_quotations(
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> list[QuotationResponse]:
    handler = ListQuotationsHandler(repository)

    quotations = handler.execute(
        ListQuotationsQuery()
    )

    return [
        quotation_to_response(quotation)
        for quotation in quotations
    ]

@router.get(
    "/{quotation_id}",
    response_model=QuotationResponse,
)
def get_quotation(
    quotation_id: UUID,
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> QuotationResponse:
    handler = GetQuotationHandler(repository)

    try:
        quotation = handler.execute(
            GetQuotationQuery(
                quotation_id=quotation_id,
            )
        )

    except QuotationNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        ) from error

    return quotation_to_response(quotation)

@router.post(
    "/{quotation_id}/items",
    response_model=QuotationItemCreatedResponse,
    status_code=201,
)
def add_quotation_item(
    quotation_id: UUID,
    request: AddQuotationItemRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> QuotationItemCreatedResponse:
    handler = AddQuotationItemHandler(repository)

    command = AddQuotationItemCommand(
        quotation_id=quotation_id,
        description=request.description,
        quantity=request.quantity,
        unit_price=request.unit_price,
        currency=request.currency,
    )

    try:
        item_id = handler.execute(command)
        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

    return QuotationItemCreatedResponse(
        id=str(item_id),
    )

@router.patch(
    "/{quotation_id}/items/{item_id}",
    status_code=204,
)
def update_quotation_item(
    quotation_id: UUID,
    item_id: UUID,
    request: UpdateQuotationItemRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> None:
    handler = UpdateQuotationItemHandler(repository)

    command = UpdateQuotationItemCommand(
        quotation_id=quotation_id,
        item_id=item_id,
        description=request.description,
        quantity=request.quantity,
        unit_price=request.unit_price,
        currency=request.currency,
    )

    try:
        handler.execute(command)
        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

@router.delete(
    "/{quotation_id}/items/{item_id}",
    status_code=204,
)
def remove_quotation_item(
    quotation_id: UUID,
    item_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> None:
    handler = RemoveQuotationItemHandler(repository)

    command = RemoveQuotationItemCommand(
        quotation_id=quotation_id,
        item_id=item_id,
    )

    try:
        handler.execute(command)
        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

@router.patch(
    "/{quotation_id}/send",
    status_code=204,
)
def send_quotation(
    quotation_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> None:
    handler = SendQuotationHandler(repository)

    try:
        handler.execute(
            SendQuotationCommand(
                quotation_id=quotation_id,
            )
        )

        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

@router.patch(
    "/{quotation_id}/accept",
    status_code=204,
)
def accept_quotation(
    quotation_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> None:
    handler = AcceptQuotationHandler(repository)

    try:
        handler.execute(
            AcceptQuotationCommand(
                quotation_id=quotation_id,
            )
        )

        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

@router.patch(
    "/{quotation_id}/reject",
    status_code=204,
)
def reject_quotation(
    quotation_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> None:
    handler = RejectQuotationHandler(repository)

    try:
        handler.execute(
            RejectQuotationCommand(
                quotation_id=quotation_id,
            )
        )

        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

@router.patch(
    "/{quotation_id}/cancel",
    status_code=204,
)
def cancel_quotation(
    quotation_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
) -> None:
    handler = CancelQuotationHandler(repository)

    try:
        handler.execute(
            CancelQuotationCommand(
                quotation_id=quotation_id,
            )
        )

        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

@router.post(
    "/{quotation_id}/convert-to-order",
    response_model=ConvertQuotationToOrderResponse,
    status_code=201,
)
def convert_quotation_to_order(
    quotation_id: UUID,
    db: Session = Depends(get_db),
    quotation_repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
    order_repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> ConvertQuotationToOrderResponse:
    handler = ConvertQuotationToOrderHandler(
        quotation_repository=quotation_repository,
        order_repository=order_repository,
    )

    command = ConvertQuotationToOrderCommand(
        quotation_id=quotation_id,
    )

    try:
        order_id = handler.execute(command)

        db.commit()

    except QuotationNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
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

    return ConvertQuotationToOrderResponse(
        order_id=str(order_id),
    )