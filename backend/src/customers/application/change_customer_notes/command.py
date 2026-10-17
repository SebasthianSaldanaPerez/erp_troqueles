from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeCustomerNotesCommand:
    customer_id: UUID
    new_notes: str | None