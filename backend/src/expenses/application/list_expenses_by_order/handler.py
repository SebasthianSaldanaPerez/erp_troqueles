from src.expenses.domain.expense import Expense
from src.expenses.domain.expense_repository import ExpenseRepository

from .query import ListExpensesByOrderQuery


class ListExpensesByOrderHandler:

    def __init__(self, repository: ExpenseRepository):
        self._repository = repository

    def execute(
        self,
        query: ListExpensesByOrderQuery,
    ) -> list[Expense]:
        return self._repository.list_by_order_id(query.order_id)