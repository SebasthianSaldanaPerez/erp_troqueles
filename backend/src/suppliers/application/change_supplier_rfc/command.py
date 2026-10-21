from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeSupplierRFCCommand:
    supplier_id: UUID
    new_rfc: str