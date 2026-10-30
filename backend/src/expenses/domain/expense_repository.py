from abc import ABC, abstractmethod
from uuid import UUID

from .expense import Expense


class ExpenseRepository(ABC):

    @abstractmethod
    def save(self, expense: Expense) -> None:
        pass

    @abstractmethod
    def get_by_id(self, expense_id: UUID) -> Expense | None:
        pass

    @abstractmethod
    def list_by_order_id(self, order_id: UUID) -> list[Expense]:
        pass