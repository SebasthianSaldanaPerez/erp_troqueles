from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.expenses.domain.expense import (
    Expense,
    ExpenseCategory,
)
from src.orders.application.errors import OrderNotFoundError
from src.orders.application.get_order_profitability.handler import (
    GetOrderProfitabilityHandler,
)
from src.orders.application.get_order_profitability.query import (
    GetOrderProfitabilityQuery,
)
from src.orders.domain.order import Order
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_expense_repository import (
    InMemoryExpenseRepository,
)
from tests.fakes.in_memory_order_repository import (
    InMemoryOrderRepository,
)


def create_order() -> Order:
    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    order.add_item(
        OrderItem(
            description="Troquel industrial",
            quantity=1,
            unit_price=Money(
                Decimal("100000.00"),
                "MXN",
            ),
        )
    )

    return order


def test_get_order_profitability():
    order_repository = InMemoryOrderRepository()
    expense_repository = InMemoryExpenseRepository()

    order = create_order()
    order_repository.save(order)

    expense_repository.save(
        Expense(
            order_id=order.id,
            description="Steel",
            amount=Money(
                Decimal("30000.00"),
                "MXN",
            ),
            category=ExpenseCategory.MATERIAL,
            expense_date=date.today(),
        )
    )

    expense_repository.save(
        Expense(
            order_id=order.id,
            description="Transport",
            amount=Money(
                Decimal("12000.00"),
                "MXN",
            ),
            category=ExpenseCategory.TRANSPORT,
            expense_date=date.today(),
        )
    )

    handler = GetOrderProfitabilityHandler(
        order_repository=order_repository,
        expense_repository=expense_repository,
    )

    result = handler.execute(
        GetOrderProfitabilityQuery(
            order_id=order.id,
        )
    )

    assert result.revenue == Decimal("100000.00")
    assert result.expenses == Decimal("42000.00")
    assert result.profit == Decimal("58000.00")
    assert result.margin == Decimal("58.00")
    assert result.currency == "MXN"

def test_cancelled_expense_is_not_included_in_profitability():
    order_repository = InMemoryOrderRepository()
    expense_repository = InMemoryExpenseRepository()

    order = create_order()
    order_repository.save(order)

    valid_expense = Expense(
        order_id=order.id,
        description="Steel",
        amount=Money(
            Decimal("30000.00"),
            "MXN",
        ),
        category=ExpenseCategory.MATERIAL,
        expense_date=date.today(),
    )

    cancelled_expense = Expense(
        order_id=order.id,
        description="Cancelled transport",
        amount=Money(
            Decimal("10000.00"),
            "MXN",
        ),
        category=ExpenseCategory.TRANSPORT,
        expense_date=date.today(),
    )

    cancelled_expense.cancel()

    expense_repository.save(valid_expense)
    expense_repository.save(cancelled_expense)

    handler = GetOrderProfitabilityHandler(
        order_repository,
        expense_repository,
    )

    result = handler.execute(
        GetOrderProfitabilityQuery(
            order_id=order.id,
        )
    )

    assert result.expenses == Decimal("30000.00")
    assert result.profit == Decimal("70000.00")
    assert result.margin == Decimal("70.0")
    
def test_get_order_profitability_raises_error_when_order_does_not_exist():
    handler = GetOrderProfitabilityHandler(
        InMemoryOrderRepository(),
        InMemoryExpenseRepository(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(
            GetOrderProfitabilityQuery(
                order_id=uuid4(),
            )
        )