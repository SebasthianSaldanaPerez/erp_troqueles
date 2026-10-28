from uuid import UUID, uuid4

from src.shared.domain.value_objects.money import Money


class OrderItem:
    def __init__(
        self,
        description: str,
        quantity: int,
        unit_price: Money,
        item_id: UUID | None = None,
    ):
        self._id = item_id or uuid4()
        self._description = self._validate_description(description)
        self._quantity = self._validate_quantity(quantity)
        self._unit_price = unit_price

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def unit_price(self) -> Money:
        return self._unit_price

    @property
    def total(self) -> Money:
        return self._unit_price.multiply(self._quantity)

    @staticmethod
    def _validate_description(description: str) -> str:
        if not description or not description.strip():
            raise ValueError("Order item description is required")

        return description.strip()

    @staticmethod
    def _validate_quantity(quantity: int) -> int:
        if quantity <= 0:
            raise ValueError("Order item quantity must be greater than zero")

        return quantity