from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeSupplierContactNameCommand:
    supplier_id: UUID
    new_contact_name: str | None