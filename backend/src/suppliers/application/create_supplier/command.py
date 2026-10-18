from dataclasses import dataclass


@dataclass(frozen=True)
class CreateSupplierCommand:
    name: str