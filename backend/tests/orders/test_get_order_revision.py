from uuid import uuid4

import pytest

from src.orders.application.errors import (
    OrderRevisionNotFoundError,
)
from src.orders.application.get_order_revision.handler import (
    GetOrderRevisionHandler,
)
from src.orders.application.get_order_revision.query import (
    GetOrderRevisionQuery,
)
from src.orders.domain.order_revision import OrderRevision
from tests.fakes.in_memory_order_revision_repository import (
    InMemoryOrderRevisionRepository,
)


def test_get_order_revision():
    repository = InMemoryOrderRevisionRepository()

    order_id = uuid4()

    revision = OrderRevision.create(
        order_id=order_id,
        revision_number=1,
        snapshot={
            "status": "CREATED",
            "total": "3480.00",
        },
        reason="Customer requested changes",
        created_by=uuid4(),
    )

    repository.save(revision)

    handler = GetOrderRevisionHandler(repository)

    result = handler.execute(
        GetOrderRevisionQuery(
            order_id=order_id,
            revision_number=1,
        )
    )

    assert result.id == revision.id
    assert result.revision_number == 1
    assert result.snapshot["total"] == "3480.00"


def test_get_order_revision_raises_error_when_not_found():
    repository = InMemoryOrderRevisionRepository()

    handler = GetOrderRevisionHandler(repository)

    with pytest.raises(OrderRevisionNotFoundError):
        handler.execute(
            GetOrderRevisionQuery(
                order_id=uuid4(),
                revision_number=99,
            )
        )