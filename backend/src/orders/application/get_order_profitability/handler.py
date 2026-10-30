from dataclasses import dataclass
from decimal import Decimal

from src.expenses.domain.expense import ExpenseStatus
from src.expenses.domain.expense_repository import ExpenseRepository
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository

from .query import GetOrderProfitabilityQuery


@dataclass(frozen=True)
class OrderProfitability:
    revenue: Decimal
    expenses: Decimal
    profit: Decimal
    margin: Decimal
    currency: str

class GetOrderProfitabilityHandler:

    def __init__(
        self,
        order_repository: OrderRepository,
        expense_repository: ExpenseRepository,
    ):
        self._order_repository = order_repository
        self._expense_repository = expense_repository

    def execute(
        self,
        query: GetOrderProfitabilityQuery,
    ) -> OrderProfitability:
        order = self._order_repository.get_by_id(query.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {query.order_id} was not found"
            )

        expenses = self._expense_repository.list_by_order_id(
            query.order_id
        )

        total_expenses = sum(
            (
                expense.amount.amount
                for expense in expenses
                if expense.status == ExpenseStatus.REGISTERED
            ),
            Decimal("0"),
        )

        revenue = order.total.amount
        profit = revenue - total_expenses

        margin = (
            (profit / revenue) * Decimal("100")
            if revenue > 0
            else Decimal("0")
        )

        return OrderProfitability(
            revenue=revenue,
            expenses=total_expenses,
            profit=profit,
            margin=margin,
            currency=order.total.currency,
        )