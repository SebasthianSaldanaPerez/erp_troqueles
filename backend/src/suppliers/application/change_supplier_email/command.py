from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeSupplierEmailCommand:
    supplier_id: UUID
    new_email: str