from datetime import date
from enum import Enum
from uuid import UUID, uuid4

from src.shared.domain.value_objects.money import Money


class ExpenseStatus(Enum):
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"


class ExpenseCategory(Enum):
    MATERIAL = "MATERIAL"
    OUTSOURCED_SERVICE = "OUTSOURCED_SERVICE"
    TRANSPORT = "TRANSPORT"
    CONSUMABLE = "CONSUMABLE"
    TOOLING = "TOOLING"
    OTHER = "OTHER"


class Expense:
    def __init__(
        self,
        order_id: UUID,
        description: str,
        amount: Money,
        category: ExpenseCategory,
        expense_date: date,
        supplier_id: UUID | None = None,
        notes: str | None = None,
        expense_id: UUID | None = None,
        status: ExpenseStatus = ExpenseStatus.REGISTERED,
    ):
        self._id = expense_id or uuid4()
        self._order_id = order_id
        self._description = self._validate_description(description)
        self._amount = amount
        self._category = category
        self._expense_date = expense_date
        self._supplier_id = supplier_id
        self._notes = notes.strip() if notes else None
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def order_id(self) -> UUID:
        return self._order_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def category(self) -> ExpenseCategory:
        return self._category

    @property
    def expense_date(self) -> date:
        return self._expense_date

    @property
    def supplier_id(self) -> UUID | None:
        return self._supplier_id

    @property
    def notes(self) -> str | None:
        return self._notes

    @property
    def status(self) -> ExpenseStatus:
        return self._status

    def cancel(self) -> None:
        if self._status == ExpenseStatus.CANCELLED:
            raise ValueError("Expense is already cancelled")

        self._status = ExpenseStatus.CANCELLED

    @staticmethod
    def _validate_description(description: str) -> str:
        if not description or not description.strip():
            raise ValueError("Expense description is required")

        return description.strip()