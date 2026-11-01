from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.expenses.domain.expense import (
    Expense,
    ExpenseCategory,
    ExpenseStatus,
)
from src.expenses.domain.expense_repository import ExpenseRepository
from src.infrastructure.database.models.expense_model import ExpenseModel
from src.shared.domain.value_objects.money import Money


class SQLAlchemyExpenseRepository(ExpenseRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, expense: Expense) -> None:
        model = self._session.get(
            ExpenseModel,
            expense.id,
        )

        if model is None:
            model = ExpenseModel(
                id=expense.id,
                order_id=expense.order_id,
                description=expense.description,
                amount=expense.amount.amount,
                currency=expense.amount.currency,
                category=expense.category.value,
                expense_date=expense.expense_date,
                supplier_id=expense.supplier_id,
                notes=expense.notes,
                status=expense.status.value,
            )

            self._session.add(model)
            return

        model.description = expense.description
        model.amount = expense.amount.amount
        model.currency = expense.amount.currency
        model.category = expense.category.value
        model.expense_date = expense.expense_date
        model.supplier_id = expense.supplier_id
        model.notes = expense.notes
        model.status = expense.status.value

    def get_by_id(
        self,
        expense_id: UUID,
    ) -> Expense | None:
        model = self._session.get(
            ExpenseModel,
            expense_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_order_id(
        self,
        order_id: UUID,
    ) -> list[Expense]:
        statement = select(ExpenseModel).where(
            ExpenseModel.order_id == order_id
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: ExpenseModel,
    ) -> Expense:
        return Expense(
            expense_id=model.id,
            order_id=model.order_id,
            description=model.description,
            amount=Money(
                amount=model.amount,
                currency=model.currency,
            ),
            category=ExpenseCategory(model.category),
            expense_date=model.expense_date,
            supplier_id=model.supplier_id,
            notes=model.notes,
            status=ExpenseStatus(model.status),
        )