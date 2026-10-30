from src.orders.application.errors import OrderNotFoundError
from src.orders.domain.order_repository import OrderRepository
from src.orders.domain.order_revision import OrderRevision
from src.orders.domain.order_revision_repository import (
    OrderRevisionRepository,
)
from src.shared.application.unit_of_work import UnitOfWork
from src.shared.domain.value_objects.money import Money

from .command import ReviseOrderCommand


class ReviseOrderHandler:

    def __init__(
        self,
        order_repository: OrderRepository,
        revision_repository: OrderRevisionRepository,
        unit_of_work: UnitOfWork,
    ):
        self._order_repository = order_repository
        self._revision_repository = revision_repository
        self._unit_of_work = unit_of_work

    def execute(self, command: ReviseOrderCommand) -> None:
        with self._unit_of_work:
            order = self._order_repository.get_by_id(command.order_id)

            if order is None:
                raise OrderNotFoundError(
                    f"Order {command.order_id} was not found"
                )

            unit_price = Money(
                amount=command.unit_price,
                currency=command.currency,
            )

            order.update_item(
                item_id=command.item_id,
                description=command.description,
                quantity=command.quantity,
                unit_price=unit_price,
            )

            revision_number = order.increment_revision()

            revision = OrderRevision.create(
                order_id=order.id,
                revision_number=revision_number,
                snapshot=order.snapshot(),
                reason=command.reason,
                created_by=command.user_id,
            )

            self._order_repository.save(order)
            self._revision_repository.save(revision)

            self._unit_of_work.commit()