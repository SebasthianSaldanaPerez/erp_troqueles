from src.expenses.application.errors import ExpenseNotFoundError
from src.expenses.domain.expense_repository import ExpenseRepository

from .command import CancelExpenseCommand


class CancelExpenseHandler:

    def __init__(self, repository: ExpenseRepository):
        self._repository = repository

    def execute(self, command: CancelExpenseCommand) -> None:
        expense = self._repository.get_by_id(command.expense_id)

        if expense is None:
            raise ExpenseNotFoundError(
                f"Expense {command.expense_id} was not found"
            )

        expense.cancel()

        self._repository.save(expense)