from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from src.expenses.domain.expense import ExpenseCategory


@dataclass(frozen=True)
class RegisterExpenseCommand:
    order_id: UUID
    description: str
    amount: Decimal
    currency: str
    category: ExpenseCategory
    expense_date: date
    supplier_id: UUID | None = None
    notes: str | None = None