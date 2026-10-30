from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.expenses.application.cancel_expense.command import (
    CancelExpenseCommand,
)
from src.expenses.application.cancel_expense.handler import (
    CancelExpenseHandler,
)
from src.expenses.application.errors import ExpenseNotFoundError
from src.expenses.domain.expense import (
    Expense,
    ExpenseCategory,
    ExpenseStatus,
)
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_expense_repository import (
    InMemoryExpenseRepository,
)


def create_expense() -> Expense:
    return Expense(
        order_id=uuid4(),
        description="Steel material",
        amount=Money(
            Decimal("5000.00"),
            "MXN",
        ),
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )


def test_cancel_expense():
    repository = InMemoryExpenseRepository()

    expense = create_expense()
    repository.save(expense)

    handler = CancelExpenseHandler(repository)

    command = CancelExpenseCommand(
        expense_id=expense.id,
    )

    handler.execute(command)

    saved_expense = repository.get_by_id(expense.id)

    assert saved_expense is not None
    assert saved_expense.status == ExpenseStatus.CANCELLED


def test_cancelled_expense_cannot_be_cancelled_again():
    repository = InMemoryExpenseRepository()

    expense = create_expense()
    expense.cancel()
    repository.save(expense)

    handler = CancelExpenseHandler(repository)

    command = CancelExpenseCommand(
        expense_id=expense.id,
    )

    with pytest.raises(ValueError):
        handler.execute(command)


def test_cancel_expense_raises_error_when_expense_does_not_exist():
    repository = InMemoryExpenseRepository()

    handler = CancelExpenseHandler(repository)

    command = CancelExpenseCommand(
        expense_id=uuid4(),
    )

    with pytest.raises(ExpenseNotFoundError):
        handler.execute(command)