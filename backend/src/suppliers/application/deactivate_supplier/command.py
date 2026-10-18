from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeactivateSupplierCommand:
    supplier_id: UUID