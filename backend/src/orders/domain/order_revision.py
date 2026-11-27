from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class OrderRevision:
    id: UUID
    order_id: UUID
    revision_number: int
    snapshot: dict
    reason: str
    created_by: UUID
    created_at: datetime

    @classmethod
    def create(
        cls,
        order_id: UUID,
        revision_number: int,
        snapshot: dict,
        reason: str,
        created_by: UUID,
    ) -> "OrderRevision":
        if revision_number <= 0:
            raise ValueError(
                "Revision number must be greater than zero"
            )

        if not reason or not reason.strip():
            raise ValueError(
                "Revision reason is required"
            )

        return cls(
            id=uuid4(),
            order_id=order_id,
            revision_number=revision_number,
            snapshot=snapshot,
            reason=reason.strip(),
            created_by=created_by,
            created_at=datetime.now(),
        )

    @classmethod
    def create_initial(
        cls,
        order_id: UUID,
        snapshot: dict,
        created_by: UUID,
    ) -> "OrderRevision":
        return cls(
            id=uuid4(),
            order_id=order_id,
            revision_number=0,
            snapshot=snapshot,
            reason="Versión inicial de la orden",
            created_by=created_by,
            created_at=datetime.now(),
        )