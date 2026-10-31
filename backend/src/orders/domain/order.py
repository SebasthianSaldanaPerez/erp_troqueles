from enum import Enum
from uuid import UUID, uuid4

from src.orders.domain.order_item import OrderItem
from src.shared.domain.value_objects.money import Money


class OrderStatus(Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class BillingStatus(Enum):
    NOT_INVOICED = "NOT_INVOICED"
    PARTIALLY_INVOICED = "PARTIALLY_INVOICED"
    FULLY_INVOICED = "FULLY_INVOICED"
    PAID = "PAID"

class Order:
    def __init__(
        self,
        customer_id: UUID,
        origin_quotation_id: UUID | None = None,
        currency: str = "MXN",
        order_id: UUID | None = None,
        revision_number: int = 0,
        status: OrderStatus = OrderStatus.CREATED,
        billing_status: BillingStatus = BillingStatus.NOT_INVOICED,
    ):
        self._id = order_id or uuid4()
        self._customer_id = customer_id
        self._origin_quotation_id = origin_quotation_id
        self._currency = currency.strip().upper()
        self._status = status
        self._billing_status = billing_status
        self._revision_number = revision_number
        self._items: list[OrderItem] = []

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def customer_id(self) -> UUID:
        return self._customer_id

    @property
    def origin_quotation_id(self) -> UUID | None:
        return self._origin_quotation_id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def items(self) -> tuple[OrderItem, ...]:
        return tuple(self._items)

    @property
    def total(self) -> Money:
        total = Money.zero(self._currency)

        for item in self._items:
            total = total.add(item.total)

        return total
    
    @property
    def revision_number(self) -> int:
        return self._revision_number

    @property
    def billing_status(self) -> BillingStatus:
        return self._billing_status

    def add_item(self, item: OrderItem) -> None:
        self._ensure_editable()

        if item.unit_price.currency != self._currency:
            raise ValueError("Order item currency must match order currency")

        self._items.append(item)

    def change_description(self, new_description: str) -> None:
        self._description = self._validate_description(new_description)

    def change_quantity(self, new_quantity: int) -> None:
        self._quantity = self._validate_quantity(new_quantity)

    def change_unit_price(self, new_unit_price: Money) -> None:
        self._unit_price = new_unit_price

    def increment_revision(self) -> int:
        self._revision_number += 1
        return self._revision_number

    def start(self) -> None:
        if self._status != OrderStatus.CREATED:
            raise ValueError("Only created orders can be started")

        if not self._items:
            raise ValueError("Order must contain at least one item")

        self._status = OrderStatus.IN_PROGRESS


    def deliver(self) -> None:
        if self._status != OrderStatus.IN_PROGRESS:
            raise ValueError("Only in-progress orders can be delivered")

        self._status = OrderStatus.DELIVERED

    def cancel(self) -> None:
        if self._status == OrderStatus.DELIVERED:
            raise ValueError("Delivered orders cannot be cancelled")

        if self._status == OrderStatus.CANCELLED:
            raise ValueError("Order is already cancelled")

        self._status = OrderStatus.CANCELLED
        
    def _ensure_editable(self) -> None:
        if self._status not in (
            OrderStatus.CREATED,
            OrderStatus.IN_PROGRESS,
        ):
            raise ValueError("Order cannot be edited in its current status")
            

    def update_item(
        self,
        item_id: UUID,
        description: str,
        quantity: int,
        unit_price: Money,
    ) -> None:
        self._ensure_editable()

        if unit_price.currency != self._currency:
            raise ValueError("Order item currency must match order currency")

        for item in self._items:
            if item.id == item_id:
                item.change_description(description)
                item.change_quantity(quantity)
                item.change_unit_price(unit_price)
                return

        raise ValueError("Order item was not found")
    
    def remove_item(self, item_id: UUID) -> None:
        self._ensure_editable()

        for item in self._items:
            if item.id == item_id:
                self._items.remove(item)
                return

        raise ValueError("Order item was not found")

    def snapshot(self) -> dict:
        return {
            "order_id": str(self._id),
            "customer_id": str(self._customer_id),
            "origin_quotation_id": (
                str(self._origin_quotation_id)
                if self._origin_quotation_id
                else None
            ),
            "status": self._status.value,
            "currency": self._currency,
            "items": [
                {
                    "id": str(item.id),
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price.amount),
                    "currency": item.unit_price.currency,
                }
                for item in self._items
            ],
            "total": str(self.total.amount),
        }
    
    def update_billing_status(
        self,
        invoiced_amount: Money,
    ) -> None:
        if invoiced_amount.currency != self._currency:
            raise ValueError("Invoiced amount currency must match order currency")

        if invoiced_amount.amount <= 0:
            self._billing_status = BillingStatus.NOT_INVOICED
            return

        if invoiced_amount.amount < self.total.amount:
            self._billing_status = BillingStatus.PARTIALLY_INVOICED
            return

        if invoiced_amount.amount == self.total.amount:
            self._billing_status = BillingStatus.FULLY_INVOICED
            return

        raise ValueError("Invoiced amount cannot exceed order total")

    def mark_as_paid(self) -> None:
        if self._billing_status != BillingStatus.FULLY_INVOICED:
            raise ValueError("Only fully invoiced orders can be marked as paid")

        self._billing_status = BillingStatus.PAID