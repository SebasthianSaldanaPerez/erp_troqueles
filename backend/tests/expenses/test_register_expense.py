from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.expenses.application.register_expense.command import (
    RegisterExpenseCommand,
)
from src.expenses.application.register_expense.handler import (
    RegisterExpenseHandler,
)
from src.expenses.domain.expense import ExpenseCategory
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order import Order
from tests.fakes.in_memory_expense_repository import (
    InMemoryExpenseRepository,
)
from tests.fakes.in_memory_order_repository import (
    InMemoryOrderRepository,
)


def test_register_expense():
    expense_repository = InMemoryExpenseRepository()
    order_repository = InMemoryOrderRepository()

    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )
    order_repository.save(order)

    handler = RegisterExpenseHandler(
        expense_repository=expense_repository,
        order_repository=order_repository,
    )

    command = RegisterExpenseCommand(
        order_id=order.id,
        description="Steel material",
        amount=Decimal("5000.00"),
        currency="MXN",
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )

    expense_id = handler.execute(command)

    expense = expense_repository.get_by_id(expense_id)

    assert expense is not None
    assert expense.order_id == order.id
    assert expense.description == "Steel material"
    assert expense.amount.amount == Decimal("5000.00")


def test_register_expense_raises_error_when_order_does_not_exist():
    expense_repository = InMemoryExpenseRepository()
    order_repository = InMemoryOrderRepository()

    handler = RegisterExpenseHandler(
        expense_repository,
        order_repository,
    )

    command = RegisterExpenseCommand(
        order_id=uuid4(),
        description="Steel material",
        amount=Decimal("5000.00"),
        currency="MXN",
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(command)