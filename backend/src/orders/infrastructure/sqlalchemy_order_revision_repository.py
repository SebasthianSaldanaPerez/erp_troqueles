from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.order_revision_model import (
    OrderRevisionModel,
)
from src.orders.domain.order_revision import OrderRevision
from src.orders.domain.order_revision_repository import (
    OrderRevisionRepository,
)


class SQLAlchemyOrderRevisionRepository(OrderRevisionRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, revision: OrderRevision) -> None:
        model = OrderRevisionModel(
            id=revision.id,
            order_id=revision.order_id,
            revision_number=revision.revision_number,
            snapshot=revision.snapshot,
            reason=revision.reason,
            created_by=revision.created_by,
            created_at=revision.created_at,
        )

        self._session.add(model)

    def list_by_order_id(
        self,
        order_id: UUID,
    ) -> list[OrderRevision]:
        statement = (
            select(OrderRevisionModel)
            .where(OrderRevisionModel.order_id == order_id)
            .order_by(OrderRevisionModel.revision_number)
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: OrderRevisionModel,
    ) -> OrderRevision:
        return OrderRevision(
            id=model.id,
            order_id=model.order_id,
            revision_number=model.revision_number,
            snapshot=model.snapshot,
            reason=model.reason,
            created_by=model.created_by,
            created_at=model.created_at,
        )