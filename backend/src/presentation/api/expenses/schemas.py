from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from src.expenses.domain.expense import ExpenseCategory


class RegisterExpenseRequest(BaseModel):
    description: str
    amount: Decimal
    currency: str = "MXN"
    category: ExpenseCategory
    expense_date: date
    supplier_id: str | None = None
    notes: str | None = None


class RegisterExpenseResponse(BaseModel):
    id: str


class ExpenseResponse(BaseModel):
    id: str
    order_id: str
    description: str
    amount: Decimal
    currency: str
    category: str
    expense_date: date
    supplier_id: str | None = None
    notes: str | None = None
    status: str