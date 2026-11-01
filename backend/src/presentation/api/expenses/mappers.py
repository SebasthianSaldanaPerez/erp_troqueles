from src.expenses.domain.expense import Expense
from src.presentation.api.expenses.schemas import ExpenseResponse


def expense_to_response(expense: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=str(expense.id),
        order_id=str(expense.order_id),
        description=expense.description,
        amount=expense.amount.amount,
        currency=expense.amount.currency,
        category=expense.category.value,
        expense_date=expense.expense_date,
        supplier_id=(
            str(expense.supplier_id)
            if expense.supplier_id
            else None
        ),
        notes=expense.notes,
        status=expense.status.value,
    )