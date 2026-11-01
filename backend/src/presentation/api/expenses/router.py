from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.expenses.application.cancel_expense.command import (
    CancelExpenseCommand,
)
from src.expenses.application.cancel_expense.handler import (
    CancelExpenseHandler,
)
from src.expenses.application.errors import ExpenseNotFoundError
from src.expenses.application.list_expenses_by_order.handler import (
    ListExpensesByOrderHandler,
)
from src.expenses.application.list_expenses_by_order.query import (
    ListExpensesByOrderQuery,
)
from src.expenses.application.register_expense.command import (
    RegisterExpenseCommand,
)
from src.expenses.application.register_expense.handler import (
    RegisterExpenseHandler,
)
from src.expenses.infrastructure.sqlalchemy_expense_repository import (
    SQLAlchemyExpenseRepository,
)
from src.orders.application.errors import OrderNotFoundError
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.presentation.api.dependencies import (
    get_db,
    get_expense_repository,
    get_order_repository,
)
from src.presentation.api.expenses.mappers import expense_to_response
from src.presentation.api.expenses.schemas import (
    ExpenseResponse,
    RegisterExpenseRequest,
    RegisterExpenseResponse,
)

router = APIRouter(
    tags=["Expenses"],
)

@router.post(
    "/orders/{order_id}/expenses",
    response_model=RegisterExpenseResponse,
    status_code=201,
)
def register_expense(
    order_id: UUID,
    request: RegisterExpenseRequest,
    db: Session = Depends(get_db),
    expense_repository: SQLAlchemyExpenseRepository = Depends(
        get_expense_repository
    ),
    order_repository: SQLAlchemyOrderRepository = Depends(
        get_order_repository
    ),
) -> RegisterExpenseResponse:
    handler = RegisterExpenseHandler(
        expense_repository=expense_repository,
        order_repository=order_repository,
    )

    command = RegisterExpenseCommand(
        order_id=order_id,
        description=request.description,
        amount=request.amount,
        currency=request.currency,
        category=request.category,
        expense_date=request.expense_date,
        supplier_id=(
            UUID(request.supplier_id)
            if request.supplier_id
            else None
        ),
        notes=request.notes,
    )

    try:
        expense_id = handler.execute(command)
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

    return RegisterExpenseResponse(
        id=str(expense_id),
    )

@router.get(
    "/orders/{order_id}/expenses",
    response_model=list[ExpenseResponse],
)
def list_expenses_by_order(
    order_id: UUID,
    repository: SQLAlchemyExpenseRepository = Depends(
        get_expense_repository
    ),
) -> list[ExpenseResponse]:
    handler = ListExpensesByOrderHandler(repository)

    expenses = handler.execute(
        ListExpensesByOrderQuery(
            order_id=order_id,
        )
    )

    return [
        expense_to_response(expense)
        for expense in expenses
    ]

@router.patch(
    "/expenses/{expense_id}/cancel",
    status_code=204,
)
def cancel_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyExpenseRepository = Depends(
        get_expense_repository
    ),
) -> None:
    handler = CancelExpenseHandler(repository)

    try:
        handler.execute(
            CancelExpenseCommand(
                expense_id=expense_id,
            )
        )

        db.commit()

    except ExpenseNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Expense not found",
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