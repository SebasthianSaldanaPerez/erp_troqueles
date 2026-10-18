import re
from dataclasses import dataclass
from src.customers.domain.errors import InvalidPhoneError


@dataclass(frozen=True)
class Phone:
    value: str

    def __post_init__(self):
        normalized_phone = re.sub(r"\D", "", self.value)

        if not normalized_phone:
            raise InvalidPhoneError("Phone cannot be empty")

        if len(normalized_phone) < 10 or len(normalized_phone) > 15:
            raise InvalidPhoneError("Invalid phone format")

        object.__setattr__(self, "value", normalized_phone)