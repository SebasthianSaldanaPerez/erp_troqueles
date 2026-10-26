from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "MXN"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

        normalized_currency = self.currency.strip().upper()

        if not normalized_currency:
            raise ValueError("Currency is required")

        object.__setattr__(self, "currency", normalized_currency)

    def add(self, other: "Money") -> "Money":
        self._validate_same_currency(other)

        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )

    def multiply(self, multiplier: int | Decimal) -> "Money":
        return Money(
            amount=self.amount * Decimal(multiplier),
            currency=self.currency,
        )

    def _validate_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("Cannot operate with different currencies")

    @classmethod
    def zero(cls, currency: str = "MXN") -> "Money":
        return cls(
            amount=Decimal("0"),
            currency=currency,
        )