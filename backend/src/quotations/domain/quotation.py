from enum import Enum
from uuid import UUID, uuid4

from src.quotations.domain.quotation_item import QuotationItem
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate


class QuotationStatus(Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class Quotation:
    def __init__(
        self,
        customer_id: UUID,
        tax_rate: TaxRate,
        currency: str = "MXN",
        quotation_id: UUID | None = None,
        status: QuotationStatus = QuotationStatus.DRAFT,
    ):
        self._id = quotation_id or uuid4()
        self._customer_id = customer_id
        self._tax_rate = tax_rate
        self._currency = currency.strip().upper()
        self._status = status
        self._items: list[QuotationItem] = []

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def customer_id(self) -> UUID:
        return self._customer_id

    @property
    def status(self) -> QuotationStatus:
        return self._status

    @property
    def items(self) -> tuple[QuotationItem, ...]:
        return tuple(self._items)

    @property
    def subtotal(self) -> Money:
        total = Money.zero(self._currency)

        for item in self._items:
            total = total.add(item.total)

        return total

    @property
    def tax(self) -> Money:
        tax_amount = self._tax_rate.apply_to(self.subtotal.amount)

        return Money(
            amount=tax_amount,
            currency=self._currency,
        )

    @property
    def total(self) -> Money:
        return self.subtotal.add(self.tax)

    def add_item(self, item: QuotationItem) -> None:
        self._ensure_editable()

        if item.unit_price.currency != self._currency:
            raise ValueError("Quotation item currency must match quotation currency")

        self._items.append(item)

    def remove_item(self, item_id: UUID) -> None:
        self._ensure_editable()

        for item in self._items:
            if item.id == item_id:
                self._items.remove(item)
                return

        raise ValueError("Quotation item was not found")

    def send(self) -> None:
        if self._status != QuotationStatus.DRAFT:
            raise ValueError("Only draft quotations can be sent")

        if not self._items:
            raise ValueError("Quotation must contain at least one item")

        self._status = QuotationStatus.SENT

    def accept(self) -> None:
        if self._status != QuotationStatus.SENT:
            raise ValueError("Only sent quotations can be accepted")

        self._status = QuotationStatus.ACCEPTED

    def reject(self) -> None:
        if self._status != QuotationStatus.SENT:
            raise ValueError("Only sent quotations can be rejected")

        self._status = QuotationStatus.REJECTED

    def cancel(self) -> None:
        if self._status not in (
            QuotationStatus.DRAFT,
            QuotationStatus.SENT,
        ):
            raise ValueError("Quotation cannot be cancelled in its current status")

        self._status = QuotationStatus.CANCELLED

    def update_item(
        self,
        item_id: UUID,
        description: str,
        quantity: int,
        unit_price: Money,
    ) -> None:
        self._ensure_editable()

        if unit_price.currency != self._currency:
            raise ValueError("Quotation item currency must match quotation currency")

        for item in self._items:
            if item.id == item_id:
                item.change_description(description)
                item.change_quantity(quantity)
                item.change_unit_price(unit_price)
                return

        raise ValueError("Quotation item was not found")

    def _ensure_editable(self) -> None:
        if self._status != QuotationStatus.DRAFT:
            raise ValueError("Only draft quotations can be edited")

