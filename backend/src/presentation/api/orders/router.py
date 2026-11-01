from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.orders.application.cancel_order.command import (
    CancelOrderCommand,
)
from src.orders.application.cancel_order.handler import (
    CancelOrderHandler,
)
from src.expenses.infrastructure.sqlalchemy_expense_repository import (
    SQLAlchemyExpenseRepository,
)
from src.orders.application.get_order_profitability.handler import (
    GetOrderProfitabilityHandler,
)
from src.orders.application.get_order_profitability.query import (
    GetOrderProfitabilityQuery,
)
from src.presentation.api.orders.schemas import (
    OrderProfitabilityResponse,
    OrderResponse,
)
from src.orders.application.deliver_order.command import (
    DeliverOrderCommand,
)
from src.orders.application.deliver_order.handler import (
    DeliverOrderHandler,
)
from src.orders.application.errors import OrderNotFoundError
from src.orders.application.get_order.handler import GetOrderHandler
from src.orders.application.get_order.query import GetOrderQuery
from src.orders.application.list_orders.handler import ListOrdersHandler
from src.orders.application.list_orders.query import ListOrdersQuery
from src.orders.application.start_order.command import (
    StartOrderCommand,
)
from src.orders.application.start_order.handler import (
    StartOrderHandler,
)
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.presentation.api.dependencies import (
    get_db,
    get_order_repository,
    get_expense_repository,
)
from src.presentation.api.orders.mappers import order_to_response
from src.presentation.api.orders.schemas import OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.get(
    "",
    response_model=list[OrderResponse],
)
def list_orders(
    repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> list[OrderResponse]:
    handler = ListOrdersHandler(repository)

    orders = handler.execute(
        ListOrdersQuery()
    )

    return [
        order_to_response(order)
        for order in orders
    ]

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: UUID,
    repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> OrderResponse:
    handler = GetOrderHandler(repository)

    try:
        order = handler.execute(
            GetOrderQuery(
                order_id=order_id,
            )
        )

    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        ) from error

    return order_to_response(order)

@router.patch(
    "/{order_id}/start",
    status_code=204,
)
def start_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> None:
    handler = StartOrderHandler(repository)

    try:
        handler.execute(
            StartOrderCommand(
                order_id=order_id,
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

@router.patch(
    "/{order_id}/deliver",
    status_code=204,
)
def deliver_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> None:
    handler = DeliverOrderHandler(repository)

    try:
        handler.execute(
            DeliverOrderCommand(
                order_id=order_id,
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

@router.patch(
    "/{order_id}/cancel",
    status_code=204,
)
def cancel_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> None:
    handler = CancelOrderHandler(repository)

    try:
        handler.execute(
            CancelOrderCommand(
                order_id=order_id,
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

@router.get(
    "/{order_id}/profitability",
    response_model=OrderProfitabilityResponse,
)
def get_order_profitability(
    order_id: UUID,
    order_repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
    expense_repository: SQLAlchemyExpenseRepository = Depends(
        get_expense_repository
    ),
) -> OrderProfitabilityResponse:
    handler = GetOrderProfitabilityHandler(
        order_repository=order_repository,
        expense_repository=expense_repository,
    )

    try:
        result = handler.execute(
            GetOrderProfitabilityQuery(
                order_id=order_id,
            )
        )

    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        ) from error

    return OrderProfitabilityResponse(
        revenue=result.revenue,
        expenses=result.expenses,
        profit=result.profit,
        margin=result.margin,
        currency=result.currency,
    )