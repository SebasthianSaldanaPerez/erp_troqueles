from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from src.orders.infrastructure.sqlalchemy_order_revision_repository import SQLAlchemyOrderRevisionRepository
from src.quotations.application.create_quotation.command import (
    CreateQuotationCommand,
)
from src.presentation.api.security import require_roles
from src.users.domain.user import User, UserRole
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.quotations.application.convert_quotation_to_order.command import (
    ConvertQuotationToOrderCommand,
)
from src.quotations.application.convert_quotation_to_order.handler import (
    ConvertQuotationToOrderHandler,
)
from src.quotations.application.reopen_quotation.command import (
    ReopenQuotationCommand,
)
from src.quotations.application.reopen_quotation.handler import (
    ReopenQuotationHandler,
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
from src.quotations.application.errors import (QuotationNotFoundError, QuotationAlreadyConvertedError,)
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
    get_order_revision_repository,
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

class QuotationOrderResponse(BaseModel):
    order_id: str | None

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
    current_user: User = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.OPERATOR,
    )
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
    current_user: User = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.OPERATOR,
        UserRole.VIEWER,
    )
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
    current_user: User = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.OPERATOR,
        UserRole.VIEWER,
    )
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
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
    current_user: User = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.OPERATOR,
    )
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
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
    current_user: User = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.OPERATOR,
    )
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
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
    revision_repository: SQLAlchemyOrderRevisionRepository = Depends(
    get_order_revision_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
    ),
) -> ConvertQuotationToOrderResponse:

    handler = ConvertQuotationToOrderHandler(
        quotation_repository=quotation_repository,
        order_repository=order_repository,
        revision_repository=revision_repository,
    )

    command = ConvertQuotationToOrderCommand(
        quotation_id=quotation_id,
        user_id=current_user.id,
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

    except QuotationAlreadyConvertedError as error:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Esta cotización ya tiene una orden generada.",
        ) from error

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        db.rollback()

        sqlstate = (
            getattr(error.orig, "sqlstate", None)
            or getattr(error.orig, "pgcode", None)
        )

        constraint_name = getattr(
            getattr(error.orig, "diag", None),
            "constraint_name",
            None,
        )

        if (
            sqlstate == "23505"
            and constraint_name == "orders_origin_quotation_id_key"
        ):
            raise HTTPException(
                status_code=409,
                detail=(
                    "Esta cotización ya tiene una orden generada."
                ),
            ) from error

        raise

    except Exception:
        db.rollback()
        raise

    return ConvertQuotationToOrderResponse(
        order_id=str(order_id),
    )

@router.patch(
    "/{quotation_id}/reopen",
    status_code=204,
)
def reopen_quotation(
    quotation_id: UUID,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
        )
    ),
    db: Session = Depends(get_db),
    repository=Depends(
        get_quotation_repository
    ),
) -> None:
    handler = ReopenQuotationHandler(
        repository
    )

    try:
        handler.execute(
            ReopenQuotationCommand(
                quotation_id=quotation_id,
            )
        )

        db.commit()

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise

@router.get(
    "/{quotation_id}/order",
    response_model=QuotationOrderResponse,
)
def get_quotation_order(
    quotation_id: UUID,
    quotation_repository: SQLAlchemyQuotationRepository = Depends(
        get_quotation_repository
    ),
    order_repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.OPERATOR,
            UserRole.VIEWER,
        )
    ),
) -> QuotationOrderResponse:

    quotation = quotation_repository.get_by_id(
        quotation_id
    )

    if quotation is None:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    order = order_repository.get_by_origin_quotation_id(
        quotation_id
    )

    return QuotationOrderResponse(
        order_id=str(order.id) if order else None
    )