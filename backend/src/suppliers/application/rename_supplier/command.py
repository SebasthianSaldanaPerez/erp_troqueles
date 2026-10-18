from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RenameSupplierCommand:
    supplier_id: UUID
    new_name: str