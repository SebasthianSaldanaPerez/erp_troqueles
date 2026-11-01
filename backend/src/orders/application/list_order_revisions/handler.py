from src.orders.domain.order_revision import OrderRevision
from src.orders.domain.order_revision_repository import (
    OrderRevisionRepository,
)

from .query import ListOrderRevisionsQuery


class ListOrderRevisionsHandler:

    def __init__(
        self,
        repository: OrderRevisionRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListOrderRevisionsQuery,
    ) -> list[OrderRevision]:
        return self._repository.list_by_order_id(
            query.order_id
        )