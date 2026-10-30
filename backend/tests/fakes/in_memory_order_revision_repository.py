from src.orders.domain.order_revision import OrderRevision
from src.orders.domain.order_revision_repository import (
    OrderRevisionRepository,
)


class InMemoryOrderRevisionRepository(OrderRevisionRepository):

    def __init__(self):
        self.revisions = []

    def save(self, revision: OrderRevision) -> None:
        self.revisions.append(revision)

    def list_by_order_id(self, order_id):
        return [
            revision
            for revision in self.revisions
            if revision.order_id == order_id
        ]