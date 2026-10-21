from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeSupplierNotesCommand:
    supplier_id: UUID
    new_notes: str | None