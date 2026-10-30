from uuid import UUID

from src.expenses.domain.expense import Expense
from src.expenses.domain.expense_repository import ExpenseRepository
from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository
from src.shared.domain.value_objects.money import Money

from .command import RegisterExpenseCommand


class RegisterExpenseHandler:

    def __init__(
        self,
        expense_repository: ExpenseRepository,
        order_repository: OrderRepository,
    ):
        self._expense_repository = expense_repository
        self._order_repository = order_repository

    def execute(self, command: RegisterExpenseCommand) -> UUID:
        order = self._order_repository.get_by_id(command.order_id)

        if order is None:
            raise OrderNotFoundError(
                f"Order {command.order_id} was not found"
            )

        amount = Money(
            amount=command.amount,
            currency=command.currency,
        )

        expense = Expense(
            order_id=command.order_id,
            description=command.description,
            amount=amount,
            category=command.category,
            expense_date=command.expense_date,
            supplier_id=command.supplier_id,
            notes=command.notes,
        )

        self._expense_repository.save(expense)

        return expense.id