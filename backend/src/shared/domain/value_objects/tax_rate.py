from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class TaxRate:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Tax rate cannot be negative")

        if self.value > 100:
            raise ValueError("Tax rate cannot be greater than 100")

    def apply_to(self, amount: Decimal) -> Decimal:
        return amount * (self.value / Decimal("100"))