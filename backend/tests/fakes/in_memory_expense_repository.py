from src.expenses.domain.expense import Expense
from src.expenses.domain.expense_repository import ExpenseRepository


class InMemoryExpenseRepository(ExpenseRepository):

    def __init__(self):
        self.expenses = []

    def save(self, expense: Expense) -> None:
        for index, existing_expense in enumerate(self.expenses):
            if existing_expense.id == expense.id:
                self.expenses[index] = expense
                return

        self.expenses.append(expense)

    def get_by_id(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense

        return None

    def list_by_order_id(self, order_id):
        return [
            expense
            for expense in self.expenses
            if expense.order_id == order_id
        ]