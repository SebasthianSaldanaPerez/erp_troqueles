from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CancelExpenseCommand:
    expense_id: UUID