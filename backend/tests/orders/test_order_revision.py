from uuid import uuid4

import pytest

from src.orders.domain.order_revision import OrderRevision


def test_order_revision_is_created():
    order_id = uuid4()
    user_id = uuid4()

    revision = OrderRevision.create(
        order_id=order_id,
        revision_number=1,
        snapshot={"total": "1000.00"},
        reason="Customer requested a quantity change",
        created_by=user_id,
    )

    assert revision.id is not None
    assert revision.order_id == order_id
    assert revision.revision_number == 1
    assert revision.snapshot == {"total": "1000.00"}
    assert revision.reason == "Customer requested a quantity change"
    assert revision.created_by == user_id
    assert revision.created_at is not None


def test_order_revision_requires_reason():
    with pytest.raises(ValueError):
        OrderRevision.create(
            order_id=uuid4(),
            revision_number=1,
            snapshot={},
            reason="",
            created_by=uuid4(),
        )


def test_order_revision_number_must_be_positive():
    with pytest.raises(ValueError):
        OrderRevision.create(
            order_id=uuid4(),
            revision_number=0,
            snapshot={},
            reason="Change",
            created_by=uuid4(),
        )