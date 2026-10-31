from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class MarkOrderAsPaidCommand:
    order_id: UUID