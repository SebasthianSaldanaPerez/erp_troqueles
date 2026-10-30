from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.expenses.domain.expense import (
    Expense,
    ExpenseCategory,
    ExpenseStatus,
)
from src.shared.domain.value_objects.money import Money


def test_expense_is_created():
    expense = Expense(
        order_id=uuid4(),
        description="Steel material",
        amount=Money(Decimal("5000.00"), "MXN"),
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )

    assert expense.id is not None
    assert expense.description == "Steel material"
    assert expense.amount.amount == Decimal("5000.00")
    assert expense.status == ExpenseStatus.REGISTERED


def test_expense_requires_description():
    with pytest.raises(ValueError):
        Expense(
            order_id=uuid4(),
            description="",
            amount=Money(Decimal("5000.00"), "MXN"),
            category=ExpenseCategory.MATERIAL,
            expense_date=date.today(),
        )


def test_expense_can_be_cancelled():
    expense = Expense(
        order_id=uuid4(),
        description="Steel material",
        amount=Money(Decimal("5000.00"), "MXN"),
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )

    expense.cancel()

    assert expense.status == ExpenseStatus.CANCELLED


def test_cancelled_expense_cannot_be_cancelled_again():
    expense = Expense(
        order_id=uuid4(),
        description="Steel material",
        amount=Money(Decimal("5000.00"), "MXN"),
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )

    expense.cancel()

    with pytest.raises(ValueError):
        expense.cancel()