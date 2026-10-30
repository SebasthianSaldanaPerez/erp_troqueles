from datetime import date
from decimal import Decimal
from uuid import uuid4

from src.expenses.application.list_expenses_by_order.handler import (
    ListExpensesByOrderHandler,
)
from src.expenses.application.list_expenses_by_order.query import (
    ListExpensesByOrderQuery,
)
from src.expenses.domain.expense import (
    Expense,
    ExpenseCategory,
)
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_expense_repository import (
    InMemoryExpenseRepository,
)


def create_expense(
    order_id,
    description: str,
    amount: str,
) -> Expense:
    return Expense(
        order_id=order_id,
        description=description,
        amount=Money(
            Decimal(amount),
            "MXN",
        ),
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )


def test_list_expenses_by_order():
    repository = InMemoryExpenseRepository()

    order_id = uuid4()
    other_order_id = uuid4()

    repository.save(
        create_expense(
            order_id=order_id,
            description="Steel",
            amount="5000.00",
        )
    )

    repository.save(
        create_expense(
            order_id=order_id,
            description="Transport",
            amount="1000.00",
        )
    )

    repository.save(
        create_expense(
            order_id=other_order_id,
            description="Other order expense",
            amount="9000.00",
        )
    )

    handler = ListExpensesByOrderHandler(repository)

    query = ListExpensesByOrderQuery(
        order_id=order_id,
    )

    expenses = handler.execute(query)

    assert len(expenses) == 2
    assert expenses[0].description == "Steel"
    assert expenses[1].description == "Transport"


def test_list_expenses_by_order_returns_empty_list():
    repository = InMemoryExpenseRepository()

    handler = ListExpensesByOrderHandler(repository)

    query = ListExpensesByOrderQuery(
        order_id=uuid4(),
    )

    expenses = handler.execute(query)

    assert expenses == []