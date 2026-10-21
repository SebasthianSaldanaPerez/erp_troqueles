from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeSupplierPhoneCommand:
    supplier_id: UUID
    new_phone: str