from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCustomerCommand:
    business_name: str