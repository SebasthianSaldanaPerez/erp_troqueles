from decimal import Decimal
from uuid import uuid4


import pytest

from src.orders.application.errors import OrderNotFoundError
from src.orders.application.revise_order.command import ReviseOrderCommand
from src.orders.application.revise_order.handler import ReviseOrderHandler
from src.orders.domain.order import Order
from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money
from tests.fakes.in_memory_order_repository import InMemoryOrderRepository
from tests.fakes.in_memory_order_revision_repository import (
    InMemoryOrderRevisionRepository,
)
from tests.fakes.in_memory_unit_of_work import InMemoryUnitOfWork

def test_revise_order():
    order_repository = InMemoryOrderRepository()
    revision_repository = InMemoryOrderRevisionRepository()
    unit_of_work = InMemoryUnitOfWork()

    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    item = OrderItem(
        description="Troquel original",
        quantity=1,
        unit_price=Money(
            Decimal("1000.00"),
            "MXN",
        ),
    )

    order.add_item(item)
    order_repository.save(order)

    handler = ReviseOrderHandler(
        order_repository=order_repository,
        revision_repository=revision_repository,
        unit_of_work=unit_of_work,
    )

    command = ReviseOrderCommand(
        order_id=order.id,
        item_id=item.id,
        description="Troquel modificado",
        quantity=2,
        unit_price=Decimal("1500.00"),
        currency="MXN",
        reason="Customer requested changes",
        user_id=uuid4(),
    )

    handler.execute(command)

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False

    saved_order = order_repository.get_by_id(order.id)
    revisions = revision_repository.list_by_order_id(order.id)

    assert saved_order is not None
    assert saved_order.revision_number == 1
    assert saved_order.items[0].description == "Troquel modificado"
    assert saved_order.items[0].quantity == 2
    assert saved_order.total.amount == Decimal("3000.00")

    assert len(revisions) == 1
    assert revisions[0].revision_number == 1
    assert revisions[0].reason == "Customer requested changes"
    assert revisions[0].snapshot["total"] == "3000.00"



def test_revise_order_raises_error_when_order_does_not_exist():
    order_repository = InMemoryOrderRepository()
    revision_repository = InMemoryOrderRevisionRepository()
    unit_of_work = InMemoryUnitOfWork()

    handler = ReviseOrderHandler(
        order_repository,
        revision_repository,
        unit_of_work
    )

    command = ReviseOrderCommand(
        order_id=uuid4(),
        item_id=uuid4(),
        description="Troquel",
        quantity=1,
        unit_price=Decimal("1000.00"),
        currency="MXN",
        reason="Change",
        user_id=uuid4(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(command)

def test_order_revisions_increment():
    order_repository = InMemoryOrderRepository()
    revision_repository = InMemoryOrderRevisionRepository()
    unit_of_work = InMemoryUnitOfWork()

    order = Order(
        customer_id=uuid4(),
        currency="MXN",
    )

    item = OrderItem(
        description="Troquel",
        quantity=1,
        unit_price=Money(Decimal("1000.00"), "MXN"),
    )

    order.add_item(item)
    order_repository.save(order)

    handler = ReviseOrderHandler(
        order_repository,
        revision_repository,
        unit_of_work
    )

    for quantity in (2, 3):
        handler.execute(
            ReviseOrderCommand(
                order_id=order.id,
                item_id=item.id,
                description="Troquel",
                quantity=quantity,
                unit_price=Decimal("1000.00"),
                currency="MXN",
                reason="Customer requested change",
                user_id=uuid4(),
            )
        )

    revisions = revision_repository.list_by_order_id(order.id)

    assert len(revisions) == 2
    assert revisions[0].revision_number == 1
    assert revisions[1].revision_number == 2

def test_revise_order_rolls_back_when_order_does_not_exist():
    order_repository = InMemoryOrderRepository()
    revision_repository = InMemoryOrderRevisionRepository()
    unit_of_work = InMemoryUnitOfWork()

    handler = ReviseOrderHandler(
        order_repository=order_repository,
        revision_repository=revision_repository,
        unit_of_work=unit_of_work,
    )

    command = ReviseOrderCommand(
        order_id=uuid4(),
        item_id=uuid4(),
        description="Troquel",
        quantity=1,
        unit_price=Decimal("1000.00"),
        currency="MXN",
        reason="Customer requested change",
        user_id=uuid4(),
    )

    with pytest.raises(OrderNotFoundError):
        handler.execute(command)

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True