from src.orders.application.errors import (
    OrderRevisionNotFoundError,
)
from src.orders.domain.order_revision import OrderRevision
from src.orders.domain.order_revision_repository import (
    OrderRevisionRepository,
)

from .query import GetOrderRevisionQuery


class GetOrderRevisionHandler:

    def __init__(
        self,
        repository: OrderRevisionRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetOrderRevisionQuery,
    ) -> OrderRevision:
        revision = (
            self._repository
            .get_by_order_id_and_revision_number(
                order_id=query.order_id,
                revision_number=query.revision_number,
            )
        )

        if revision is None:
            raise OrderRevisionNotFoundError(
                f"Revision {query.revision_number} "
                f"for order {query.order_id} was not found"
            )

        return revision