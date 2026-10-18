from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ReactivateSupplierCommand:
    supplier_id: UUID